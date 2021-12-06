# Specifikation
## Inledning:
Min idé är att skapa en visuell simulering av kön till ett imaginärt postkontor. Simuleringen kommer ha en standard fördelningsfunktion av antal ärenden för varje kund, men användaren kommer kunna sätta egna värden på sannolikheten att en kund har x antal ärenden. Ibland kommer köflödet störas av rånaren, och i slutet av dagen kommer statistiken visas.
### De möjliga svårigheterna är:
1.)        Att begränsa värden på fördelningsfunktionen. Användaren ska bara kunna sätta värden som leder till att summan av alla sannolikheter för x antal ärenden blir 100%.
2.) Logiken för rånaren är någorlunda komplex, eftersom flera variabler ändras samtidigt och programmet blir mer dynamiskt. Därför kommer den biten kräva mer tid att implementera.

## Användarscenarier:
### Se köflödet med standardparametrar: 
Användaren öppnar programmet och trycker på knappen ”Start” utan att mata in egna parametrar. Då körs simuleringen med standardfördelningsfunktionen som ges av (0.5)^x där x är antal ärenden, t.ex. kommer ½ av alla kunder ha 1 ärende. Användaren får se hur kön flöder. Ibland kommer rånaren och då kan användaren åskåda hur köflödet påverkas av detta. Användaren tittar på statistiken som visas upp efter att dagen är slut och stänger programmet.
### Simulera kön med parameterjusteringar: 
Användaren startar programmet, justerar reglaget som ändrar sannolikheten att en kund med x antal ärenden inträffar och trycker på ”Start”. Användaren studerar visuellt hur köflödet beror på antal kunder med ett visst antal ärenden och även på om störningar i form av rån förekommer. Användaren får statistik i slutet av dagen, den här gången stänger användaren av förekomsten av rånaren och klickar ”Start”. Efter simuleringen är klar väljer användaren att stänga programmet.
### Studera statistik: 
Användaren startar programmet och väljer egna parametrar genom att sätta sannolikheten på att förekomsten av kunder med 1 ärende till 20%,                2 ärenden till 30%, 3 ärenden till 10%, 4 till 5% och 5+ ärenden till 35%. Därefter klickar hen på ”Start”-knappen. Simuleringen körs och användaren får se hur kön flöder genom dagen. Efter simuleringen får användaren statistiken över dagen och antecknar den. Simuleringen körs en gång till med sannolikheten att kunder med 1 ärende är 100%. Användaren antecknar statistiken igen och jämför hur fördelningen påverkade den genomsnittliga väntetiden per kund. Därefter stänger användaren programmet.

## Programskelett
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
## Dataflöde:
Programmet börjar med att placera i de globala variablerna i minnet, sedan skapas ett officeobjekt. Officeobjektet innehåller status (antingen är dörren öppen eller stängd), tiden per ärende och en lista av nuvarande kunder. Varje kund innehåller sin färg, tid som hen kom in, positionen i kön, antal ärenden och om hen är en rånare. Användaren presenteras med en meny där hen kan justera värden på sannolikheten att en ny kund dyker upp varje minut, förekomsten av rån, hur ofta kontoret lyckas försvara sig, hur ofta kunder dör i ett rån OSV. Därefter körs simulationen och varje minut kallas funktionen spawn_client som med sannolikheten given av N_client_probability kommer skapa ett objekt Client med slumpmässig färg, antal ärenden och om hen är en rånare. Objektet placeras i minnet i listan clients hos Office-objektet och funktionen serve körs. Efter ett visst antal minuter som ges av t_task tas objektet bort från listan clients, variablerna Tot_num_clients, Tot_await_time som ansvarar för statistiken uppdateras samt nästa kund börjar betjänas. När tiden blir 1800 ändras status hos office-objektet till 0, alla kunder i clients betjänas och sedan visas statistiken på skärmen.

