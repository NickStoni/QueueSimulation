import PySimpleGUI as sg
import random
from default_vars import *
import matplotlib.pyplot as plt

def gen_color():
    """Generates a random color"""
    r = lambda: random.randint(50,255)
    return '#%02X%02X%02X' % (r(),r(),r())

def plot(waiting_time,clients):
    """Shows a plots of average waiting time and number of clients in the store throughout the simulation cycle"""
    x=[i for i in range(len(waiting_time))]

    plt.figure()

    plt.subplot(121)
    plt.plot(x, waiting_time)
    plt.title('Average waiting time')
    ax = plt.gca()
    ax.axes.xaxis.set_visible(False)

    plt.subplot(122)
    plt.plot(x, clients)
    plt.title('N. clients in the store')
    ax = plt.gca()
    ax.axes.xaxis.set_visible(False)

    plt.show()

class Bubble:
    """Class Bubble visualises its parent (class Client), contains parameters as parent, graph, robber, x,y,
    as well as functions to handle Bubble (move, delete etc)"""
    def __init__(self,graph, parent):
        self.graph=graph
        self.parent=parent

        self.robber=hasattr(self.parent, 'body_count')

        self.x = WIN_X//2
        self.y = WIN_Y - 80 - 40 * (parent.position_queue-1)

        self.draw_client()
        self.draw_client_text()

    def draw_client(self):
        """Draws the coloured bubble for a client, robber and dead client"""
        col_in = gen_color()
        col_out = gen_color()
        rad=CLIENT_BUBBLE_RADIUS
        if self.robber:
            col_in = "red"
            col_out = col_in
        elif not self.parent.alive:
            rad = CLIENT_BUBBLE_RADIUS + 2
            col_in = "black"
            col_out = col_in

        self.circle = sg.Graph.DrawCircle(self.graph, fill_color=col_in, center_location=(self.x, self.y),
                                   line_color=col_out, line_width=4, radius=rad)

    def draw_client_text(self):
        """Draws text representing number of tasks of parent or 'X' if parent is a robber"""
        self.text = sg.Graph.DrawText(self.graph, ((self.robber and "X") or self.parent.tasks),
                                 location=(self.x, self.y), color="black", angle=0)

    def refresh(self):
        """Checks if Bubble has to be updated according to the status of simulation and
        handles the refreshment of visual representation"""
        if self.robber:
            self.rob()
            return
        elif not self.parent.alive:
            self.remove_client_bubble()
            self.draw_client()
            return

        self.update_text()
        prev_y=self.y
        self.y = WIN_Y - 80 - 40 * (self.parent.position_queue - 1)
        if prev_y != self.y:
            self.move_client_bubble()

    def rob(self):
        """If parent is a robber, he/she will be placed in the middle of the screen"""
        self.y = WIN_Y//2
        self.x = WIN_X//2
        self.move_client_bubble()

    def move_client_bubble(self):
        """Moves the client bubble with text displaying number of tasks to the x and y location,
        representing his/her position in the queue"""
        sg.Graph.RelocateFigure(self.graph, self.circle, x=self.x - CLIENT_BUBBLE_RADIUS,
                                y=self.y + CLIENT_BUBBLE_RADIUS)
        sg.Graph.RelocateFigure(self.graph, self.text, x=self.x, y=self.y)

    def update_text(self):
        """Handles refreshment of displaying number of tasks the parent has"""
        sg.Graph.delete_figure(self.graph, self.text)
        self.text = sg.Graph.DrawText(self.graph, self.parent.tasks, location=(self.x, self.y),
                             color="black", angle=0)

    def remove_client_bubble(self):
        """Takes care of removing the bubble from the screen"""
        sg.Graph.delete_figure(self.graph, self.text)
        sg.Graph.delete_figure(self.graph, self.circle)

    def escape(self):
        """Bubble moves chaotically, happens when there is a robber present."""
        rand_x=int(random.randrange(-70,70))
        rand_y=int(random.randrange(0,50))
        self.x=self.x+rand_x
        self.y=self.y+rand_y

class Office:
    """Class is a visual representation of the office box. Contains graph, world, name and rectangle.
    also methods to put office on screen and update text (called when bonus is activated or expired)"""
    def __init__(self,graph,world,name=OFFICE_NAME):
        self.graph=graph
        self.world = world
        self.name=name
        self.rectangle, self.text = self.draw_office()

    def draw_office(self):
        """Draws the office box with text inside it"""
        rectangle = sg.Graph.DrawRectangle(self.graph, top_left=((WIN_X // 2) - 60, WIN_Y - 10),
                                           bottom_right=((WIN_X // 2) + 60, WIN_Y - 40), line_color=gen_color(),
                                           fill_color=gen_color())
        text = sg.Graph.DrawText(self.graph,self.name, location=((WIN_X // 2), WIN_Y - 25), font=("Helvetica", 15))
        return rectangle,text

    def update_text(self,won=True,expired=False):
        """Updates text colour by deleting the text element and returning a new one with updated colour"""
        color="red"
        if won:
            color="green"
        if expired:
            color="black"
        sg.Graph.delete_figure(self.graph, self.text)
        self.text = sg.Graph.DrawText(self.graph, self.name, location=((WIN_X // 2), WIN_Y - 25),
                          color=color, angle=0, font=("Helvetica", 15))

class Window:
    """Class generates a window with the given layout and contains a method (refresh) to enable the user
    modify specific parameters through interaction with the window"""
    def __init__(self,layout,world):
        self.window = sg.Window(OFFICE_NAME, layout, font=("Helvetica", 13), finalize=True)
        self.world=world
        self.graph = self.window.Element("-GRAPH-")
        self.office = Office(self.graph,self.world)

        self.world.graph=self.graph
        self.world.office=self.office

    def refresh(self):
        """Refreshes values of the variables that affect the simulation, by read off the values from the window
        and updates displayment of the statistics of the simulation """
        event, values = self.window.Read(timeout=int(1000 * self.world.speed))
        self.window.Refresh()
        self.window["-TIME-"].update(self.world.time.time)
        self.world.mins_per_task = int(values["-TTASK-"])
        self.world.speed = 1 / (values["speed"])
        self.world.max_clients = values["max_clients"]
        self.world.robberies_enabled = values["-IFROB-"]
        self.world.protect_probability = values["-PROTPROB-"] / 100
        self.world.client_shot_probability = values["-SHOTPROB-"] / 100
        self.world.default_taskgen = values["-DEFPROBMETH-"]
        self.world.robbery_rate = 1 / values["-ROBFREQ-"]
        self.world.mean = values["-CUSPROBM-"]
        self.world.standard_deviation = values["-CUSPROBSD-"]
        self.window["-AVEWAIT-"].update(round(self.world.ave_waiting_time,2))
        self.window["-CLIENTS-"].update(self.world.clients_today)
        self.window["-WAIT-"].update(self.world.clients_waiting_time.time)
        self.window["-DEAD-"].update(self.world.total_dead_count)

        if not self.world.bonus:
            self.world.chance_of_client = 1 / values["-TCLIENT-"]
            self.window['-TCLIENT-'].update(disabled=False)
            self.office.update_text(expired=True)
        else:
            self.window['-TCLIENT-'].update(disabled=True)

        if self.world.done:
            self.office.update_text(expired=True)

        if event == "Exit" or event == sg.WIN_CLOSED:
            quit()
        elif event == "START":
            self.world.office_open=True

"""Defines the GUI layout"""
sg.theme("DarkTeal9")

serve_frame=[sg.Frame("Serve speed",[
    [sg.Text('Time per task (mins)',justification='center'),
     sg.Slider(range=(1,15), default_value=int(mins_per_task), orientation='h',key="-TTASK-")]])]

arrival_frame=[sg.Frame("Arrival delay",[
    [sg.Text('Client arrives after (mins)',justification='center'),
    sg.Slider(range=(1,30), default_value=int(1/chance_of_client), orientation='h',key="-TCLIENT-")]])]

robberies_frame=[sg.Frame("Robberies",[[sg.Checkbox('Robberies can occur', default=robberies_enabled, key="-IFROB-")],
       [sg.Text('Robberies occur 1 in',justification='center'),
        sg.Slider(range=(1,3000), default_value=int(1/robbery_rate), orientation='h',key="-ROBFREQ-")],
       [sg.Text('Office defends (%)',justification='center'),
        sg.Slider(range=(0,100), default_value=int(protect_probability*100), orientation='h',key="-PROTPROB-")],
       [sg.Text('Risk to die (%)',justification='center'),
        sg.Slider(range=(0,100), default_value=int(client_shot_probability*100), orientation='h',key="-SHOTPROB-")]])]

task_gen_frame=[sg.Frame("Task generation",[
        [sg.Text("Function for task gen"),
         sg.Radio('Standard', "-PROBMeth-", key="-DEFPROBMETH-", default=True),
         sg.Radio('Custom', "-PROBMeth-",key="-CUSPROBMETH-",)],
        [sg.Text("Standard deviation"),
         sg.Slider(range=(1,5),default_value=standard_deviation,resolution=0.1,key="-CUSPROBSD-",orientation='h')],
         [sg.Text("Mean"),
          sg.Slider(range=(1.2,15.0),default_value=mean,resolution=0.1,key="-CUSPROBM-",orientation='h')]])]

parameters=[serve_frame,arrival_frame,robberies_frame,task_gen_frame]

top_line=[sg.Text('Time'), sg.Text("-", key='-TIME-'),
           sg.Text('Clients'), sg.Text("-", key='-CLIENTS-'),
           sg.Text('Waiting time'), sg.Text("-", key='-WAIT-'),
           sg.Text('Ave waiting time'), sg.Text("-", key='-AVEWAIT-'),
           sg.Text('Dead'), sg.Text("-", key="-DEAD-")]

bottom_line=[sg.Button('START',button_color="green"),sg.Exit(),
             sg.Text("Speed"),
             sg.Slider(range=(0.5,300.0),resolution=0.1,default_value=speed,key="speed",orientation="h"),
             sg.Text('Max clients'),
             sg.Slider(range=(1,100),resolution=1,default_value=max_clients,key="max_clients",orientation="h")]

layout = [top_line,
          [sg.Graph((WIN_X, WIN_Y), (0, 0), (WIN_X, WIN_Y), background_color='lightblue', key='-GRAPH-'),
           sg.Column(parameters)],
          bottom_line]