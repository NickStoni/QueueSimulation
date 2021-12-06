import math
import numpy as np
import client
import graphics
import default_vars as vars

class TimeManagement:
    """TimeManagement takes care of displaying time strings properly and handling time increments,
    contains parameters as time, normalise, h, m"""
    def __init__(self,time="00:00", normalise=False):
        self.time=time
        self.normalise = normalise
        self.h, self.m = map(int, self.time.split(':'))

    def __add__(self, other):
        """Manages time increments by a determined number of minutes, if normalise is True, then
        time is normalised, that is 24 is the highest value and 00 comes after that"""
        t = self.h * 60 + self.m + other
        h, m = divmod(t, 60)
        if self.normalise:
            h%=24
        time="{:02d}:{:02d}".format(h, m)
        return TimeManagement(time,normalise=self.normalise)

    def get_minutes(self):
        """Converts time to number of minutes"""
        return (self.m + self.h*60)


class World:
    """Class World takes care of the back end processes. World contains all dynamic variables that
    the user can change during the simulation, and statistical variables. World also contains
    functions that handle the simulation"""
    def __init__(self):
        self.office_name = vars.OFFICE_NAME
        self.open_time = TimeManagement(vars.OPEN_TIME,normalise=True)
        self.close_time = TimeManagement(vars.CLOSE_TIME)
        self.speed = vars.speed
        self.max_clients = vars.max_clients
        self.chance_of_client = vars.chance_of_client
        self.mins_per_task = vars.mins_per_task
        self.default_taskgen = vars.default_taskgen
        self.mean = vars.mean
        self.standard_deviation = vars.standard_deviation
        self.robberies_enabled = vars.robberies_enabled
        self.robbery_rate = vars.robbery_rate
        self.protect_probability = vars.protect_probability
        self.client_shot_probability = vars.client_shot_probability

        self.office_open = False
        self.done = False
        self.time = TimeManagement(vars.OPEN_TIME,normalise=True)
        self.current_clients = list()

        self.clients_today = 0
        self.clients_waiting_time = TimeManagement()
        self.ave_waiting_time = 0
        self.instantaneous_ave_waiting_time = list()
        self.total_dead_count = 0
        self.instantaneous_clients= list()

        self.robbery_mode = False
        self.bonus = False
        self.bonus_decline_rate = 1
        self.bonus_time_finish = TimeManagement()

        self.graph=None
        self.office=None

    def update_stats(self):
        """Updates time and statistics"""
        self.time += 1

        clients_in_queue = len(self.current_clients)-1
        clients_in_queue = max(clients_in_queue,0)

        self.instantaneous_clients.append(len(self.current_clients))
        self.instantaneous_ave_waiting_time.append(self.ave_waiting_time)

        if not self.robbery_mode:
            self.clients_waiting_time += clients_in_queue
            self.ave_waiting_time = self.clients_waiting_time.get_minutes()/max(self.clients_today,1)

    def reset(self):
        """Resets all statistical variables and the window"""
        self.time = self.open_time
        self.clients_today = 0
        self.clients_waiting_time = TimeManagement()
        self.ave_waiting_time = 0
        self.instantaneous_ave_waiting_time = list()
        self.total_dead_count = 0
        self.instantaneous_clients = list()
        self.bonus=False
        self.chance_of_client=vars.chance_of_client
        self.done=False

    def generate_tasks(self):
        """Generates number of tasks for a client, based on the default_taskgen parameter"""
        if self.default_taskgen:
            probability = np.random.uniform(0, 1)
            n = -math.log(probability, 2)
            return int(max(1, math.ceil(n)))
        else:
            n = np.random.normal(self.mean, self.standard_deviation, 1)
            return int(max(1,n))

    def process_robbery(self):
        """Handles the process of robbery. Clients try to survive during the process, if they die
        the dead_count of the robber is updated. If the time of robbery is out, the process finishes and
        the robber leaves."""
        robber = self.current_clients[len(self.current_clients) - 1]
        if vars.GRAPHICS_MODE:
            self.update_client_bubble()
        if self.time.time==robber.time_done.time:
            robber.done()
            self.robbery_mode = False
            self.total_dead_count += robber.body_count
            self.remove_clients()
            return

        clients_now=len(self.current_clients)-1
        for i in range(clients_now):
            if self.current_clients[i].alive:
                dead = not self.current_clients[i].attempt_survive()
                robber.body_count += dead

    def manage_bonus(self):
        """Adjusts bonus and disables it when time of bonus is out. For GRAPHICS_MODE disables also
        ability to chance frequency of client arrival and updates text color of the office box"""
        self.chance_of_client -= self.bonus_decline_rate
        if self.time.time == self.bonus_time_finish.time:
            self.bonus = False
            if not vars.GRAPHICS_MODE:
                self.chance_of_client=vars.chance_of_client

    def remove_clients(self):
        """Removes all clients from the list and the window"""
        if vars.GRAPHICS_MODE:
            for client in self.current_clients:
                client.done()
        self.current_clients = list()

    def serve(self):
        """Serves clients, that is completes their tasks, and refreshes the visual representation.
        If robber is present calls process_robbery instead."""
        if not len(self.current_clients):
            return
        if self.robbery_mode:
            self.process_robbery()
            return
        if vars.GRAPHICS_MODE:
            self.update_client_bubble()
        client_at_counter = self.current_clients[0]
        if not client_at_counter.time_done:
            client_at_counter.time_done = self.time+(self.mins_per_task)
        self.refresh_client_tasks(client_at_counter)

    def refresh_client_tasks(self,client):
        """Handles the decrement of tasks for client. If the time of the task
        has run out decreases tasks by 1 and if all tasks are complete the client leaves"""
        if client.time_done.time == self.time.time:
            client.time_done=self.time+(self.mins_per_task)
            client.tasks-=1
            if client.tasks==0:
                self.client_finished()

    def client_finished(self):
        """Handles removal of the client from world and moves every client up the queue."""
        self.current_clients[0].done()
        del self.current_clients[0]
        for client in self.current_clients:
            client.position_queue-=1

    def update_client_bubble(self):
        """Refreshes visual representation of clients"""
        for client in self.current_clients:
            client.bubble.refresh()

    def try_spawn_client(self):
        """According to the given probability, generates an instance of a client with color,
        tasks or a robber if robberies are enabled and adds them to world current_clients"""
        if not self.office_open or len(self.current_clients)>=self.max_clients:
            return None
        random_number = np.random.uniform()

        if (self.chance_of_client > random_number):
            self.clients_today+=1
            spawn_robber = self.robberies_enabled and bool(np.random.uniform()<float(self.robbery_rate)) and not self.bonus
            if spawn_robber:
                new_client = client.Robber(self, self.graph)
                self.robbery_mode=True
            else:
                tasks = self.generate_tasks()
                new_client = client.Client(self, tasks, self.graph)
            new_client.enter()
            self.current_clients.append(new_client)

    def fight_robber(self):
        """When the robbery is to be finished the function is called. Decides whether
        the robber has won or lost the battle against the cashier and enables the bonus accordingly."""
        won = bool(float(self.protect_probability)>np.random.uniform())
        self.bonus = True
        self.bonus_time_finish = self.time + vars.DELTA_BONUS

        if vars.GRAPHICS_MODE:
            self.office.update_text(won)
        self.chance_of_client=vars.chance_of_client
        if won:
            msg = "slagit"
            self.bonus_decline_rate = self.chance_of_client*(vars.BONUS_WON - 1) / vars.DELTA_BONUS
            self.chance_of_client *= vars.BONUS_WON
            return msg
        else:
            msg = "misslyckats döda"
            self.bonus_decline_rate = self.chance_of_client*(vars.BONUS_LOST -1) / vars.DELTA_BONUS
            self.chance_of_client *= vars.BONUS_LOST
            return msg

    def check_time_close(self):
        """Checks if it is time for office to be closed and closes office if it is.
        If none clients are left the statistics is shown."""
        if self.time.time==self.close_time.time:
            self.office_open=False
            if not vars.GRAPHICS_MODE:
                close_string="Kl. {} stängs dörren".format(self.time.time)
                print(close_string)
        if not self.office_open and not len(self.current_clients):
            self.show_stats()
            self.done=True

    def show_stats(self):
        """Shows the statistics collected during the simulation cycle."""
        total_waiting_time=self.clients_waiting_time.get_minutes()
        if vars.GRAPHICS_MODE:
            graphics.plot(self.instantaneous_ave_waiting_time,self.instantaneous_clients)
        else:
            stats_string="STATISTIK: {} kunder, kundväntetid {} minuter = {:.2f} minuter/kund, {} kunder har dött".format(
                self.clients_today,total_waiting_time,self.ave_waiting_time,self.total_dead_count)
            print(stats_string)
            done_string = "Alla kunder förutsätts anlända vid hela minuttider, ingen får \n" \
                        "komma indräljande några sekunder för tidigt eller för sent!"
            print(done_string)