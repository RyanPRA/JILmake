# Import the __future__ and six modules to provide Python 3 syntax and compatability.
import __future__
import six

# Import OrderedDict and yaml modules for use with YAML interaction.
from collections import OrderedDict
import yaml

# Sources 
# https://stackoverflow.com/questions/44765482/multiple-constructors-the-pythonic-way

# Create a global variable with a list that contains the order in which Autosys Job fields should be listed in the JIL file.
global order_global 
order_global = ['insert_job','job_type','owner','permission','max_run_alarm','alarm_if_fail',
                'send_notification','box_name','machine','condition','file_watch','command',
                'watch_file_min_size','std_err_file','watch_interval']

# Create class AutosysJob
class AutosysJob(object):

    """Parent class that is primarily designed to accept the default properties for Autosys Jobs start.

    Args:
        1.  insert_job: String
        2.  job_type: String
        3.  owner: String
        4.  permission: String
        5.  max_run_alarm: Integer
        6.  alarm_if_fail: Boolean
        7.  send_notification: Boolean
    
    Returns:
        Instance of AutosysJob object 

    """

    def __init__(self, insert_job=None, job_type=None, owner=None, permission=None, max_run_alarm=None, 
                alarm_if_fail=None, send_notification=None):
        
        self.insert_job = insert_job
        self.job_type = job_type
        self.owner = owner
        self.permission = permission
        self.max_run_alarm = max_run_alarm
        self.alarm_if_fail = alarm_if_fail
        self.send_notification = send_notification


# Create AutosysBoxJob class 
class AutosysBoxJob(AutosysJob):

    """Subclass of AutosysJob class that accepts the properties for Autosys Jobs and 
        has a default of "BOX" for job_type. Represents an Autosys job of type "BOX"

    Args:
        1.  insert_job: String
        2.  owner: String
        3.  permission: String
        4.  max_run_alarm: Integer
        5.  alarm_if_fail: Boolean
        6.  send_notification: Boolean
    
    Returns:
        Instance of AutosysBoxJob object 

    """

    def __init__(self, insert_job=None, job_type=None, owner=None, permission=None, max_run_alarm=None, 
                 alarm_if_fail=None, send_notification=None):
            
        super(AutosysBoxJob, self).__init__(insert_job, job_type, owner, permission, max_run_alarm, 
              alarm_if_fail, send_notification)

        self.job_type = 'BOX'


# Create AutosysFWJob class 
class AutosysFWJob(AutosysJob):

    """Subclass of AutosysJob class that accepts the properties for Autosys Jobs and 
        has a default value of "FW" for job_type. Represents an Autosys job of type "FW"
        Note also that the AutosysFWJob has new parameters beginning at number 7 
        that are not present in the AutosysJob class parent.

    Args:
        1.  insert_job: String
        2.  owner: String
        3.  permission: String
        4.  max_run_alarm: Integer
        5.  alarm_if_fail: Boolean
        6.  send_notification: Boolean

        7.  box_name: String
        8.  machine: String
        9.  file_watch: String
        10. watch_file_min_size: Integer
        11. watch_interval: Integer
    
    Returns:
        Instance of AutosysFWJob object 

    """

    def __init__(self, insert_job=None, job_type=None, owner=None, permission=None, max_run_alarm=None, 
                 alarm_if_fail=None, send_notification=None, box_name=None, machine=None, file_watch=None,
                 watch_file_min_size=None, watch_interval=None):
            
        super(AutosysFWJob, self).__init__(insert_job, job_type, owner, permission, max_run_alarm, 
              alarm_if_fail, send_notification)

        self.job_type = 'FW'
        self.box_name = box_name 
        self.machine = machine 
        self.file_watch = file_watch
        self.watch_file_min_size = watch_file_min_size
        self.watch_interval = watch_interval

# Create AutosysCmdJob class 
class AutosysCmdJob(AutosysJob):

    """Subclass of AutosysJob class that accepts the properties for Autosys Jobs and 
        has a default value of "CMD" for job_type. Represents an Autosys job of type "CMD"
        Note also that the AutosysCmdJob has new parameters beginning at number 7 
        that are not present in the AutosysJob class parent.

    Args:
        1.  insert_job: String
        2.  owner: String
        3.  permission: String
        4.  max_run_alarm: Integer
        5.  alarm_if_fail: Boolean
        6.  send_notification: Boolean

        7.  box_name: String
        8.  machine: String
        9.  condition: String
        10.  command: String
        11.  std_err_file: String
    
    Returns:
        Instance of AutosysCmdJob object 

    """

    def __init__(self, insert_job=None, job_type=None, owner=None, permission=None, max_run_alarm=None, 
                 alarm_if_fail=None, send_notification=None, box_name=None, machine=None, condition=None,
                 command=None, std_err_file=None):
            
        super(AutosysCmdJob, self).__init__(insert_job, job_type, owner, permission, max_run_alarm, 
              alarm_if_fail, send_notification)

        self.job_type = 'CMD'
        self.box_name = box_name 
        self.machine = machine 
        self.condition = condition
        self.command = command
        self.std_err_file = std_err_file

# Create AutosysProcess class 
class AutosysAny(object):

    """Creates an Autosys Job object with any and only the parameters specified by the user. 
    Args:
        Any number of parameters that togeather constitute an AutosysJob object 
    
    Returns:
        Instance of AutosysAny object 

    """

    def __init__(self, **kwargs):

        for key, val in kwargs.items():
            exec("self." + key + '=val')

# Create AutosysProcess class 
class AutosysProcess(object):

    """Consolidates AutosysJob objects into a single process flow.

    Args:
            Comma-separated list of AutosysJob objects.
        OR:
            Use the .from_yaml method to construct the list of AutosysJob objects from a YAML file.
            Specify the path/filename/extension of the YAML file.  
            For example: my_directory/my_file.yml.

    Returns:
        Instance of AutosysProcess object 

    """

    # Default constructor, collects comma-separated list of AutosysJob objects.
    def __init__(self, *args):

        self.objects = args

    # Alternative constructor, creates object of data from YAML file
    @classmethod
    def from_yaml(cls, filename):
        
        with open(filename, 'r') as file:
            objects = OrderedDict(yaml.load(file))

        # Create a list to store objects 
        total_objects = []
        for obj in objects.keys():
            d = {}
            for key, value in zip(objects[obj].keys(), objects[obj].values()): 
                d.update({key:value})

            # Store instances of each new Autosys object in a list 
            total_objects.append(AutosysAny(**d))

        return cls(*total_objects)

    # Render Autosys Process 
    def render(self):

        """Render the objects into the JIL format.

        Args:
            None

        Returns:
            A string that contains Autosys job object content organized in JIL format. 

        """

        output = ""
        for obj in self.objects:
            instance = "/* -- " + str(obj.insert_job) + " -- */\n\n"
            #Order parameters that are defined in global_order 
            for key in order_global:
                for var, value in vars(obj).items():
                    if key == var:
                        instance += str(str(var) + ": " + str(value) + "\n")
            #Add any remaining parameters that are not defined in global_order to the end 
            for var, value in vars(obj).items():
                if var not in instance:
                    instance += str(str(var) + ": " + str(value) + "\n")
            output += str(instance + "\n")
        
        return output

    def write(self, write_file):

        """Writes the rendered objects to a .jil file.

        Args:
            1. Desired location and filename as a string. 
            For example:
                "user/directory/filename"

        Returns:
            Creates a .jil file in the path/filename specified. 

        """

        with open(write_file, "w") as text_file:
            text_file.write(self.render())

print("----------------------------------------------Let's do some informal testing to demonstrate functionality!-------------------------------------------------------")

# test_job1 is an AutosysJob
test_job1 = AutosysJob(insert_job="test_job1", job_type="test job", owner="user", permission="yes", send_notification="y")
print(test_job1.insert_job, test_job1.job_type, test_job1.owner, test_job1.permission, test_job1.max_run_alarm, test_job1.alarm_if_fail, test_job1.send_notification)
assert(test_job1.max_run_alarm == None)

# test_job2 is an AutosysBoxJob
test_job2 = AutosysBoxJob(insert_job="test_job2", owner="user", permission="yes", max_run_alarm=15, alarm_if_fail="y", send_notification="y")
print(test_job2.insert_job, test_job2.job_type, test_job2.owner, test_job2.permission, test_job2.max_run_alarm, test_job2.alarm_if_fail, test_job2.send_notification)
assert(test_job2.job_type == "BOX")

# test_job3 is an AutosysFWJob
test_job3 = AutosysFWJob(insert_job="test_job3", owner="user", permission="yes", max_run_alarm=15, alarm_if_fail="y", send_notification="y", box_name="my_box",
                         machine = "my_computer", watch_file_min_size=7, watch_interval=3)
print(test_job3.insert_job, test_job3.job_type, test_job3.owner, test_job3.permission, test_job3.max_run_alarm, test_job3.alarm_if_fail, 
      test_job3.box_name, test_job3.machine, test_job3.file_watch, test_job3.watch_file_min_size, test_job3.watch_interval)
assert(test_job3.job_type == "FW")
assert(test_job3.file_watch == None)

# test_job4 is an AutosysCMDJob
test_job4 = AutosysCmdJob(insert_job="test_job4", owner="user", permission="yes", max_run_alarm=15, alarm_if_fail="y", send_notification="y", box_name="my_box",
                         machine = "my_computer", condition="my_cond", command="my_comm")
print(test_job4.insert_job, test_job4.job_type, test_job4.owner, test_job4.permission, test_job4.max_run_alarm, test_job4.alarm_if_fail, 
      test_job4.box_name, test_job4.machine, test_job4.condition, test_job4.command, test_job4.std_err_file)
assert(test_job4.job_type == "CMD")
assert(test_job4.std_err_file == None)

# test_job5 is an AutosysAny Job
test_job5 = AutosysAny(insert_job='test_job5', random="this_is_random_param")
print(test_job5.insert_job, test_job5.random)

# Let's test AutosysProcess class by passing our Autosys objects to it and rendering the process flow
test_process = AutosysProcess(test_job1, test_job2, test_job3, test_job4, test_job5)
print(test_process.render())

# Lastly, let's use the .write module to write this output to a file called JIL_test.jil, check the current directory for the output file
test_process.write('JIL_test.jil')

# Now that that's done, let's test this with a YAML file. Use the from_yaml module of AutosysProcess to create Autosys objects from the YAML file - jiltest.yml
test_yaml = AutosysProcess.from_yaml('jiltest.yml')
print(test_yaml.render())

# Finally let's write these to a file called JIL_test_yml.jil
test_yaml.write("JIL_test_yml.jil")

# That's all folks 
