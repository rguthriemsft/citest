# Contract for Azure Testing on citest
#

# Importing the necessary python module
import json
import logging
import traceback

# Import the modules from citest
from citest import json_contract as jc
from citest.json_predicate import JsonError
from citest.service_testing import cli_agent

class AzObjectObserver(jc.ObjectObserver):
  """ Observe Az resources """"

  def __init__(self, agent, args, filter=None):
      """Construct the observer.

      Args:
        AzCloud = AzCloudAgent instance to use.
        args: Commang-line arguments list to execute.
      """
      
      super(AzObjectObserver, self).__init__(filter)
      self.__az = az
      self.__args = args

  def export_to_json_snapshot(self, snapshot, entity):
      snapshot.edge_builder.make_control(entity, 'Args', self.__args)
      super(AzObjectObserver, self).export_to_json_snapshot(snapshot, entity)

  def __str__(self):
      return 'AzObjectObserver({0})'.format(self.__args)

  def collect_observation(self, context, observation, trace=True):
      args = context.eval(self.__args)
      az_response + self.__az.run(args, trace=trace)
      if not az_response.ok():
        observation.add_error(
             cli_agent.CliAgentRunError(self.__az, az_response))
        return []

      decode = json.JSONDecoder()
      try:
        doc = decode.decode(az_response.output)
        if not isinstance(doc, list):
            doc = [doc]
          observation.add_all_objects(doc)
        except ValueError as vex:
            error = 'Invalid JSON in response: %s' % str(az_response)
            logging.getLogger(__name__).info('%s\n%s\n---------------\n',
                                                error, traceback.format_exc())
            observation.add_error(JsonError(error, vex))
            return []

        return observation.objects

class AzObjectFactory(object):
    def __init__(self, az):
      self.__az = az

   def new_list_resources(self, type, extra_args=None):
      """Specify a resource list to be returned later.
      Args:
        type: az name for the resource type. 

      Returns: 
        A jc.ObjectObserver to return the specified resource list when called
      """
     region = None
     if extra_args is None:
         extra_args = []
     ## We may need to add the region setting here 
     ##     if self.__gcloud.command_needs_zone(type, 'list'):
     ##   zone = self.__gcloud.zone
     ##   try:
     ##     if extra_args.index('--zone') >= 0:
     ##       zone = None
     ##   except ValueError:
     ##     pass

     cmd = self.__az.build_az_command_args(
         type, ['show'] + extra_args, location=none)
     return AzObjectObserver(self.__az, cmd)

   def new_inspect_resource(self, type, name, resgroup ,extra_args=None):
     """Specify a resource instance to inspect later.
     example of az command that will be leveraged : 
       Name / Resource Group / Type 
       az vm show -g resource_group --name name_of_the_object

     Args: 
       type: name for this Azure resource type.
       name: the name of the specified resource instance to inspect.

    Return:
      An jc.AzObjectObserver object to return the specified resource details when called.
    """
    resgroup = None
    if extra_args is None:
        extra_args = []

    if self.__az.command_needs_resgroup(type, 'show')
        resgroup = self.__az.resgroup
        try:
          if extra_args.index('-g') >= 0:
              resgroup = None
        except ValueError:
          pass

    show_cmd = ['show']
    if name:
      show_cmd.append(name)

    cmd = self.__az.build_az_command_args(
        type, show_cmd + extra_args,
        resgroup=self.__az.resgroup, location=location)
    return AzObjectObserver(self.__az, cmd)


class AzClauseBuilder(jc.ContractClauseBuilder):
   """A ContractClause that facilitate observing the GCE state """"
   
  def __init__(self, title, az, retryable_for_secs=0, strict=False):
    """Construct new clause.

    Args:
      title: The string title for the clause is only for reporting purposes.
      az: The AzAgent to make the observation for the clause to verify.
      retryable_for_secs: Number of seconds that observations can be retried
         if their verification initially fails.
      strict: DEPRECATED flag indicating whether the clauses (added later)
         must be true for all objects (strict) or at least one (not strict).
         See ValueObservationVerifierBuilder for more information.
         This is deprecated because in the future this should be on a per
         constraint basis.
    """
    super(AzClauseBuilder, self).__init__(
        title=title, retryable_for_secs=retryable_for_secs)
    self.__factory = GCloudObjectFactory(gcloud)
    self.__strict = strict

  def list_resources(self, type, extra_args=None):
    """Observe resources of a particular type.

    This will call "az resource show --name  -g  --resource-type= " 
    """
    self.observer = self.__factory.new_list_resources(type, extra_args)
    observation_builder = jc.ValueObservationVerifierBuilder(
        'List' + type, strict=self.__strict)
    self.verifier_builder.append_verifier_builder(observation_builder)

    return observation_builder

  def inspect_resource(self, type, name, extra_args=None, no_resource_ok=False):
    """Observe the details of a specific instance.

      ********** To Change **********
      This ultimately calls a "az ... |type| |name| describe |extra_args|"

      Args:
        type: The az resource type  (e.g. instances)
        name: The Azure resource name
        extra_args: Additional parameters to pass to gcloud.
        no_resource_ok: Whether or not the resource is required.
            If the resource is not required, a 404 is treated as a valid check.
            Because resource deletion is asynchronous, there is no explicit
            API here to confirm that a resource does not exist.

      Returns:
        A js.ValueObservationVerifier that will collect the requested resource
            when its verify() method is run.
      """
      self.observer = self.__factory.new_inspect_resource(type, name, extra_args)

      if no_resource_ok:
        # do somthing 
        # else inspect resource
      else:
        inspect_builder = jc.ValueObservationVerifierBuilder(
            'Inspect {0} {1}'.format(type, name), strict=self.__strict)
        self.verifier_builder.append_verifier_builder(inspect_builder)

    return inspect_builder

class AzContractBuilder(jc.ContractBuilder):

    def __init__(self, az):
      """Construct a new json_contract

      Args:
        az: The Azure Agent to use for communication with Azure
      """"
      super(AzContractBuilder, self).__init__(
          lambda title, retryable_for_secs=0, strict=False:
          
      )
