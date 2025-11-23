import threading
import time
from queue import Queue
import os
from src.serv_core.run_server import runServer
from src.serv_core.close_server import closeServer
from  src.data_core.get_data import getData
from src.config_core.config_handler import configHandler, setConfigValue
from src.plugin_core.plugin_handler import pluginUpdate

GAME_STATE_QUEUE: Queue[dict[str, bool | float | dict[str, float]]] = Queue() 
""" Used to share game state data between server and AI/display threads. """
ACTION_QUEUE: Queue[dict[str, float |str]] = Queue()
""" Used to send inputs to server thread"""
CMD_QUEUE: Queue[str] = Queue()
""" Used to send commands between threads. """
STOP_EVENT = threading.Event()
""" Security event to stop all threads when needed (stopping all threads inside cmd thread). """
STOP_SERVER = threading.Event()
""" Event to stop server thread if needed. """
STOP_DISPLAY = threading.Event()
""" Event to stop display thread if needed. """
STOP_AI = threading.Event()
""" Event to stop AI thread if needed. """

"""
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
THREADS
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
"""
def serverThreadFunc():
    """ Server thread function to handle socket connection and data reception. """
    conn = runServer()
    CMD_QUEUE.put('continue')
    try:
        if conn:
            conn.settimeout(0.1) 
    except Exception as e:
        print(f"\tSERVER > /!\\ Warning /!\\ - Could not set socket timeout: '{e}'")
        pass

    while not STOP_EVENT.is_set() and not STOP_SERVER.is_set()  :
        try:
            data = getData(conn)
            GAME_STATE_QUEUE.put(data)
            if not CMD_QUEUE.empty():
                cmd = CMD_QUEUE.get()
                if cmd == 'quit':
                    STOP_EVENT.set()
                    break
                
            if not ACTION_QUEUE.empty():
                action = ACTION_QUEUE.get()

        except TimeoutError:
            pass 
        except Exception as e:
            print(f"\tSERVER > Error or client disconnected: '{e}'")
            STOP_EVENT.set()
            
        finally:
            time.sleep(0.001) 

    closeServer(conn)
    CMD_QUEUE.put('continue')
    return


def aiThreadFunc():
    """ Not implemented yet. Implement before use. """
    print("\tAI > Started.")
    
    while not STOP_EVENT.is_set() and not STOP_AI.is_set():
        if not GAME_STATE_QUEUE.empty():
            state_data = GAME_STATE_QUEUE.get()


    print("\tAI > Stopped.")
    return


def displayThreadFunc():
    """ Not implemented yet. Implement before use. """
    print("\tDISPLAY > Started.")
    CMD_QUEUE.put('continue')
    
    while not STOP_EVENT.is_set() and not STOP_DISPLAY.is_set():
        if not GAME_STATE_QUEUE.empty():
            state_data = GAME_STATE_QUEUE.get()
            GAME_STATE_QUEUE.put_nowait(state_data)

        time.sleep(0.1)

    print("\tDISPLAY > Stopped.")
    CMD_QUEUE.put('continue')
    return


"""
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
COMMAND FUNCTIONS
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
"""
COMPONENT_MAP = {
    "server": serverThreadFunc,
    "display": displayThreadFunc,
    # "ai": aiThreadFunc,
}

STOP_MAP = {
    "server": STOP_SERVER,
    "display": STOP_DISPLAY,
    "ai": STOP_AI,
}

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
    return

def startComponent(name: str, threads: dict[str, threading.Thread]):
    """Creates and starts a thread for a given component if it's not already active."""
    if name in threads and threads[name].is_alive():
        print(f"\tComponent '{name}' is already ACTIVE.")
        CMD_QUEUE.put('continue')
        return

    targetFunc = COMPONENT_MAP.get(name)
    if not targetFunc:
        print(f"\t Unknown component: '{name}'. Use 'run help' for a list of available components.")
        CMD_QUEUE.put('continue')
        return

    try:
        newThread = threading.Thread(target=targetFunc, name=f"{name.capitalize()}Thread")
        newThread.daemon = True
        threads[name] = newThread
        newThread.start()
        print(f"\tComponent '{name}' started.")
        
    except Exception as e:
        print(f"\tError starting '{name}': {e}")


def handleStopComponent(name: str, threads: dict[str, threading.Thread]):
    """ Stops a specific component thread if it's active. For now, individual stopping is not supported. """
    if len(name) < 1:
        print("\tSpecify component to stop (e.g., stop server).")
        return
    if name in threads and threads[name].is_alive():
        STOP_MAP[name].set()
        threads[name].join()
        print(f"\tComponent '{name}' has been stopped.")
    else:
        print(f"\tComponent '{name}' is not active or does not exist.")


def handleStatus(threads: dict[str, threading.Thread]):
    """Displays the status of active components."""
    statusMessages: list[str] = []
    
    # Iterate through active threads dictionary
    for name, thread in threads.items():
         statusMessages.append(f"\t| {thread.name}\t| {'ACTIVE' if thread.is_alive() else 'INACTIVE'}\t|")

    cmdThread = threading.current_thread()
    statusMessages.append(f"\t| {cmdThread.name}\t| ACTIVE\t|")
    
    print("\n\t---- ACTIVE COMPONENT STATUS ----")
    print("\n".join(statusMessages))
    print("\t---------------------------------\n")



"""
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
COMMAND THREAD
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
"""
def cmdThreadFunc(threads: dict[str, threading.Thread]):
    """ Command thread function to handle user inputs and manage components. """
    cmdCounter = 0
    config = configHandler()
    print(f"CMD[{cmdCounter}]> Started. Type 'help' for command list.")
    while not STOP_EVENT.is_set():
        try:
            fullCommand = input(f"CMD[{cmdCounter}]> ").strip().lower()
            commandParts = fullCommand.split()
            if not commandParts:
                continue
            commandKey, mainArg, others = commandParts[0], commandParts[1] if len(commandParts) > 1 else None, commandParts[2:] if len(commandParts) > 2 else []
            if fullCommand == "help":
                print("\tAvailable commands:")
                print("\t - run [component_name]: Start a component.")
                print("\t - stop [component_name]: Stop a component.")
                print("\t - status: Show status of active components.")
                print("\t - clear: Clear the console.")
                print("\t - quit or q: Quit the application.")
                CMD_QUEUE.put('continue')
            elif fullCommand == "teapot":
                print("\tI am a Tea Pot!")
                CMD_QUEUE.put('continue')
            elif fullCommand == "config":
                print("\tCurrent Configuration:")
                for key, value in config.items():
                    print(f"\t - {key}: {value}")
                CMD_QUEUE.put('continue')
            elif fullCommand == "update":
                pluginUpdate(config)
                CMD_QUEUE.put('continue')
            elif fullCommand == "quit" or fullCommand == "q":
                STOP_EVENT.set()
                for t in threads.values():
                    if t.is_alive():
                        print(f"\tWaiting for '{t.name}' to stop...")
                        t.join()
                CMD_QUEUE.put('continue')
            elif commandKey == "clear":
                clear()
                CMD_QUEUE.put('continue')
            elif commandKey == "status":
                handleStatus(threads)
                CMD_QUEUE.put('continue')
            elif commandKey == "run":
                if mainArg in COMPONENT_MAP:
                    startComponent(mainArg, threads)
                elif mainArg == "help":
                    print("\tUsage: run [component_name]")
                    print("\tAvailable components: " + ", ".join(COMPONENT_MAP.keys()))
                    CMD_QUEUE.put('continue')
                else:
                    print(f"\tUnknown component '{mainArg}'. Use 'run help' for a list of available components.")
                    CMD_QUEUE.put('continue')
            elif commandKey == "stop":
                if mainArg in STOP_MAP:
                    handleStopComponent(mainArg, threads)
                elif mainArg == "help":
                    print("\tUsage: stop [component_name]")
                    print("\tAvailable components: " + ", ".join(COMPONENT_MAP.keys()))
                    CMD_QUEUE.put('continue')
                else:
                    print(f"\tUnknown component '{mainArg}'. Use 'stop help' for a list of available components.")
                    CMD_QUEUE.put('continue')

            while CMD_QUEUE.empty() or CMD_QUEUE.get_nowait() != 'continue':
                continue
            cmdCounter += 1
            
        except EOFError:
            break
        except KeyboardInterrupt:
            break

    STOP_EVENT.set()
    print("CMD > Stopped.")



def main():
    """ Main function to start the command thread and manage application lifecycle. """
    print("PyMania> Application started.")
    threads: dict[str, threading.Thread] = {}

    cmdT = threading.Thread(target=cmdThreadFunc, name="CmdThread", args=(threads,))
    cmdT.daemon = True
    cmdT.start()

    try:
        while not STOP_EVENT.is_set():
            time.sleep(1)
            if not cmdT.is_alive():
                break
    except KeyboardInterrupt:
        print("\tKeyboardInterrupt : Ctrl+C.")
        STOP_EVENT.set()
    finally:
        for t in threads.values():
            if t.is_alive():
                t.join()
        if cmdT.is_alive():
            cmdT.join()
        print("PyMania> Application terminated.")
        exit(0)


if __name__ == "__main__":
    main()