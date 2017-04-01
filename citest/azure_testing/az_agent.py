# Create the base agent for Azure CITest scenario 

# Import the needed python modules 
import logging
import sys
import argparse
import json

from citest.base.json_scrubber import JsonScrubber
from citest.service_testing import cli_agent

class AzAgent(cli_agent.CliAgent):
    """ The Agent that uses az 2.0 cli to interact with Azure Cloud.

    Attributes:
      ***** Define here the needed attributes *******
      subscription: The default subscription to use 
      location: The default location to use
    """

    def __init__(self, trace=True):
        """ Construct the instance 

        Args: 
            location: The Azure region to use by default
            trace: Wether to trace all I/O by default
        """

        super(AzAgent, self).__init__('az')
        self.trace = trace
        self.logger = logging.getLogger(__name__)

    def build_az_command_args(self, az_resource, az_command, args):

        """"Build the Azure command line to be used
        Args:
        action: 
        Returns:
     
        return [action] + ([resource] if resource else []) + (args if args else [])
        """

        preamble = []
        globalcmd = [az_resource, az_command] + args
        return preamble + globalcmd
        

    def run_resource_list_commandline(self, command_args, trace=True):
        """Runs the given command and returns the json resouce list.

        Args:
            command_args: The commandline returned by the build_az_command_args
        Raises:
            ValueError if the command fails
        Returns:
            List of objects from the command.
        """
        # This is where login should happen 

        az_response = self.run(command_args, trace)
        if not az_response.ok():
            # TODO(Insert code here to login to Azure)
            raise ValueError(az_response.error)

        decoder = json.JSONDecoder()
        doc = decoder.decode(az_response.output)
        # The following line is from the aws_agent
        # return doc[root_key] if root_key else doc
        
        return doc

    def get_resource_list(self, az_group, az_subgroup, az_command, args, trace=True):

        """Returns a resource list returned when executing the aws commandline.

        This is a combination of build_az_command_args and
        run_resource_list_commandline.
        """
        # The context is used by citest for it's execution context

        args = context.eval(args)
        args = self.build_az_command_args(az_group=az_group,
                                        az_subgroup=az_subgroup,
                                        az_command=az_command,
                                        args=args)
        return self.run_resource_list_commandline(args, trace=trace)



# def main():
#     """Trying the azure agent code"""
#     import az_agent
#     az = az_agent.AzAgent("westus")

#     parser = argparse.ArgumentParser()
#     parser.add_argument("-SPN")
#     parser.add_argument("-SPNSecret")
#     parser.add_argument("-TenantID")
#     args = parser.parse_args()

#     az_args = ['vm', 'list']
#     az_params = ['--output', 'json']

#     #cmdline = az.build_az_command_args('', 'vm', 'list', az_params)
#     listvm = az.get_resource_list('storage', 'account', 'list', [])
#     print listvm
    


# if __name__ == '__main__':
#   sys.exit(main())
