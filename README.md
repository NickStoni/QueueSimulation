# Specification
## Introduction:
My idea is to create a visual simulation of a queue at an imaginary post office. The simulation will have a standard distribution function of the number of tasks for each customer, but the user will be able to set their own values ​​for the probability that a customer has x number of tasks. Sometimes the queue flow will be disrupted by the robber, and at the end of the day, the statistics will be displayed.
### Possible difficulties:
1.) Limiting the values ​​of the distribution function. The user should only be able to set values ​​that result in the sum of all probabilities for x number of tasks being 100%.

2.) The logic for the robber is somewhat complex, as several variables change simultaneously, and the program becomes more dynamic. Therefore, that part will require more time to implement.

## User Scenarios:
### View the queue flow with default parameters:
The user opens the program and presses the "Start" button without entering their own parameters. Then the simulation runs with the default distribution function given by (0.5)^x where x is the number of tasks, for example, half of all customers will have 1 task. The user gets to see how the queue flows. Sometimes the robber appears, and then the user can observe how the queue flow is affected by this. The user looks at the statistics displayed at the end of the day and closes the program.
### Simulate the queue with parameter adjustments:
The user starts the program, adjusts the slider that changes the probability that a customer with x number of tasks occurs, and presses "Start". The user visually studies how the queue flow depends on the number of customers with a certain number of tasks and also on whether disturbances in the form of robberies occur. The user receives statistics at the end of the day, this time the user turns off the presence of the robber and clicks "Start". After the simulation is complete, the user chooses to close the program.
### Study statistics:
The user starts the program and selects their own parameters by setting the probability of the occurrence of customers with 1 task to 20%, 2 tasks to 30%, 3 tasks to 10%, 4 tasks to 5%, and 5+ tasks to 35%. Then the user clicks the "Start" button. The simulation runs, and the user gets to see how the queue flows throughout the day. After the simulation, the user receives statistics for the day and notes them down. The simulation runs again with the probability of customers with 1 task set to 100%. The user notes the statistics again and compares how the distribution affected the average waiting time per customer. Then the user closes the program.

## Program Skeleton
```
"Global parameters"
Run_speed = 1
N_client_probability=1/5
Bonus=False
Rate_robbery=1/1000
Protect_probability=2/3
Prob_shot=1/10
Custom_prob=False
Prob_1_task=0.5
Prob_2_tasks=0.25
Prob_3_tasks=0.125
Prob_4_tasks=0.125/2
Prob_5m_tasks=0.125/4

"Global stat variables"
Time = 900
Tot_num_clients = 0
Tot_await_time = 0

class Client:
    """Clients fill up the queue and await their tasks to be done"""

    def __init__(self, color, arr_time, pos_queue, n_tasks, if_robber=False):
        """Spawn a client with a color, pos_queue, n_tasks and if_robber.
        The if_robber parameter default is set to False."""
        self.color=color
        self.arr_time=arr_time
        self.pos_queue = pos_queue
        self.n_tasks = n_tasks
        self.if_robber = if_robber

    def move_forward(self):
        """Move forward one step in the queue.
        The function is called when the previous client was served."""
        pass

    def rob(self):
        """If if_robber set to True the client will run chaotically
        and perform the robbery before disappearing"""
        pass

    def escape(self):
        """The client runs away without awaiting his turn.
        Happens when there is a robber present."""
        pass

    def esc_fail(self):
        """The client fails to escape and is shot."""
        pass

    def done(self):
        """The client moves away, when his tasks are complete.
        Called when pos_queue is set to 0."""
        pass

class Office(object):
    """Office is responsible for managing clients."""

    def __init__(self, status=0, t_task=2, clients=[]):
        """Office contains status (the door is either open or closed),
        t_task and a list of clients"""
        self.status=status
        self.t_task=t_task
        self.clients = clients

    def if_protect(self,protect_prob):
        """When there is a robber, the office tries to protect itself.
        Which will affect the rate at which clients arrive.
        Returns either True or False"""
        pass

    def calc_t_done(self,t_task):
        """Calculates the time when the task will be complete"""
        pass

    def serve(self):
        """Serves the current client, allows each client to move up the queue."""
        pass

    def update_stat(self):
        "After each client is served the global daily statistics is updated."
        pass

def gen_num_tasks():
    """Generates number of tasks for a client"""
    pass

def gen_color():
    """Generates a random color"""
    pass

def spawn_client():
    "Generates an instance of a client with color, tasks and if he is a robber"
    pass

def affect_rate_arr_minute():
    """Changes probability a client arrives per minute,
    either higher or lower rate. Happens after a robbery."""
    pass

def calc_average_await_t():
    """Calculates average waiting time"""
    pass
```
## Data Flow:
The program starts by placing the global variables in memory, then an office object is created. The office object contains status (whether the door is open or closed), the time per task, and a list of current customers. Each customer contains their color, arrival time, position in the queue, number of tasks, and whether they are a robber. The user is presented with a menu where they can adjust values ​​for the probability that a new customer appears every minute, the occurrence of robberies, how often the office successfully defends itself, how often customers die in a robbery, etc. Then the simulation runs, and every minute the spawn_client function is called, which with the probability given by N_client_probability will create a Client object with a random color, number of tasks, and whether they are a robber. The object is placed in memory in the clients list of the Office object, and the serve function is called. After a certain number of minutes given by t_task, the object is removed from the clients list, the variables Tot_num_clients, Tot_await_time responsible for statistics are updated, and the next customer begins to be served. When the time reaches 1800, the status of the office object changes to 0, all customers in clients are served, and then the statistics are displayed on the screen.
