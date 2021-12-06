import default_vars as vars
import graphics
import world

def await_start():
    """Checks if the office has been open: sets office to open directly for terminal mode and
    checks if the button START has been pressed for graphics mode"""
    if not vars.GRAPHICS_MODE:
        world.office_open=True
        return
    window.refresh()

def simulation():
    """The function executes the helper functions in the right sequence to proceed the simulation one step forward.
    First a new client is attemped to be spawn if a robbery is not ongoing. Then all clients are served,
    and if bonus is active then the function to manage its decrement is called. After that the statistics is updated,
    and the function to check if it's time to close office is called. If graphics mode is enabled,
    the window is refreshed to represent current cycle of simulation."""
    if not world.robbery_mode:
        world.try_spawn_client()
    world.serve()
    if world.bonus:
        world.manage_bonus()
    world.update_stats()
    world.check_time_close()
    if vars.GRAPHICS_MODE:
        window.refresh()

if __name__ == "__main__":
    world = world.World()
    single_run = not vars.GRAPHICS_MODE
    if vars.GRAPHICS_MODE:
        window = graphics.Window(graphics.layout, world)

    while True:
        while not world.office_open:
            await_start()

        while not world.done:
            simulation()

        if not single_run:
            world.reset()
        else:
            break