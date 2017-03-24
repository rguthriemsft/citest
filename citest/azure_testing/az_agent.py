# Create the base agent for Azure CITest scenario 

# Import the needed python modules 
import logging

from citest.base.json_scrubber import JsonScrubber
from citest.service_testing import cli_agent

class AzAgent(cli_agent.CliAgent):
    """ The Agent that uses az 2.0 cli to interact with Azure Cloud.

    Attributes:
      ***** Define here the needed attributes *******
      subscription: The default subscription to use 
      location: The default location to use
    """
    @property
    def location(self):
        """ The Azure location to use for the test """
        return self.__location

    def __init__(self, location, resgroup, trace=True):
        """ Construct the instance 

        Args: 
            location: The Azure region to use by default
            trace: Wether to trace all I/O by default
        """

        super(AzAgent, self).__init__('az', output_scrubber=JsonScrubber())
        self.__location = location
        self.__resgroup = resgroup
        self.trace = trace
        self.logger = logging.getLogger(__name__)
        
    def build_az_command_args(self, az_command, args, resgroup=None, location=None):

        """"

    Args:
      action: The operation we are going to perform on the resource.
      resource: The kubectl resource we are going to operate on (if applicable).
      args: The arguments following [gcloud_module, gce_type].
    Returns:
      list of complete command line arguments following implied 'kubectl'
      return [action] + ([resource] if resource else []) + (args if args else [])
      """


        if not location:
            location = self.__location
        
        preamble = []
        if resgroup:
            preamble += ['--resource-group', resgroup]
        if location:
            preamble += ['--location', location]
        return az_command + args

    def run_resource_list_commandline(self, command_args, trace=True):
        """Runs the given command and returns the json resouce list.

        Args:
            command_args: The commandline returned by the build_az_command_args
        Raises:
            ValueError if the command fails
        Returns:
            List of objects from the command.
        """
        az_response = self.run(command_args, trace)
        if not az_response.ok():
            raise ValueError(az_response.error)

        decoder = json.JSONDecoder()
        doc = decoder.decode(az_response.output)
        # The following line is from the aws_agent
        # return doc[root_key] if root_key else doc
        return doc

    def get_resource_list(self, context, format='json'):
        cmdline = 'az group list'
        return self.run(cmdline, trace=self.trace)
