import graphics
import default_vars as vars
import numpy as np

class Client:
    """Clients fill up the queue and await their tasks to be done. Client contains such properties as world, tasks,
    arrival_time, number, positio_queue, time_done, alive and bubble if visual representation is enabled."""
    def __init__(self, world,tasks,graph=None):
        self.world=world
        self.tasks=tasks
        self.arrival_time=world.time
        self.number=world.clients_today
        self.position_queue=len(world.current_clients)+1
        self.time_done = 0
        self.alive = True
        if vars.GRAPHICS_MODE:
            self.bubble=graphics.Bubble(graph,self)

    def done(self):
        """Called when client has no tasks left. Handles the removal of a single client."""
        if vars.GRAPHICS_MODE:
            self.bubble.remove_client_bubble()
        else:
            leave_string = "Kl. {} går kund {} ".format(self.world.time.time, self.number)
            if len(self.world.current_clients) > 1:
                leave_string += "och kund {} blir betjänad".format(self.number + 1)
            print(leave_string)

    def attempt_survive(self):
        """During a robbery the client is attempting to survive. The function determines if the client is
        still alive."""
        alive = bool(np.random.uniform() > float(self.world.client_shot_probability))
        self.alive = alive
        if alive and vars.GRAPHICS_MODE:
            self.bubble.escape()
        return alive

    def enter(self):
        """Called when the client is spawned. The function takes care of letting the user know
        that the client is present, by printing a message if graphics is disabled."""
        if not vars.GRAPHICS_MODE:
            client_string = "Kl. {} kommer kund {} ({} är.) ".format(self.arrival_time.time, self.number, self.tasks)
            queue = "och ställer sej i kön som nr {}.".format(len(self.world.current_clients))
            if self.position_queue == 1:
                queue = "och blir genast betjänad."
            client_string += queue
            print(client_string)

class Robber:
    """Represents a robber with a unique property body_count, also contains properties as
    world, arrival_time, time_done, position_queue and bubble if GRAPHICS_MODE is enabled"""
    def __init__(self, world, graph=None):
        self.world = world
        self.arrival_time=world.time
        self.time_done=world.time+vars.DELTA_ROBBERY
        self.body_count = 0
        self.position_queue = len(world.current_clients) + 1
        if vars.GRAPHICS_MODE:
            self.bubble = graphics.Bubble(graph,self)

        self.world.robbery_finish_time = self.world.time + vars.DELTA_ROBBERY

    def done(self):
        """When the robbery is over, the function is called and the robber is removed. Prints the result
        of the robbery if the simulation is run in terminal mode"""
        leave_message = self.world.fight_robber()
        if vars.GRAPHICS_MODE:
            self.bubble.remove_client_bubble()
        else:
            leave_string = "Kl. {} har kassörskan {} rånaren i {}".format(self.time_done.time,leave_message,
                                                                    self.world.office_name)
            leave_string_2 = "{} kund/er har dött under rånet".format(self.body_count)
            print(leave_string)
            print(leave_string_2)

    def enter(self):
        """Called when the robber is spawned, prints a response message to the user in terminal mode"""
        if not vars.GRAPHICS_MODE:
            robber_string = "Kl. {} kommer en rånare".format(self.arrival_time.time)
            print(robber_string)