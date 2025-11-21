import threading
import time
from queue import Queue
import os
from src.serv_core.run_server import runServer
from src.serv_core.close_server import closeServer
from  src.data_core.get_data import getData

GAME_STATE_QUEUE: Queue[dict[str, bool | float | dict[str, float]]] = Queue() 
ACTION_QUEUE: Queue[dict[str, float |str]] = Queue()
CMD_QUEUE: Queue[str] = Queue()
STOP_EVENT = threading.Event()


"""
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
THREADS
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
"""
def serverThreadFunc():
    conn = runServer()
    CMD_QUEUE.put('continue')
    print("\tSERVER THREAD: Started.")
    try:
        if conn:
            conn.settimeout(0.1) 
    except Exception as e:
        print(f"\tSERVER THREAD: Warning - Could not set socket timeout: {e}")
        pass

    while not STOP_EVENT.is_set():
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
            print(f"\tSERVER THREAD: Error or client disconnected: {e}")
            STOP_EVENT.set()
            
        finally:
            time.sleep(0.001) 

    closeServer(conn)
    print("SERVER: Stopped.")
    return


def aiThreadFunc():
    print("AI Thread: Started.")
    
    while not STOP_EVENT.is_set():
        if not GAME_STATE_QUEUE.empty():
            state_data = GAME_STATE_QUEUE.get()


    print("AI Thread: Stopped.")
    return


def displayThreadFunc():
    print("Display Thread: Started.")
    CMD_QUEUE.put('continue')
    
    while not STOP_EVENT.is_set():
        if not GAME_STATE_QUEUE.empty():
            state_data = GAME_STATE_QUEUE.get()
            GAME_STATE_QUEUE.put_nowait(state_data)

        time.sleep(0.1)

    print("Display Thread: Stopped.")
    return


"""
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
COMMAND FUNCTIONS
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
"""
COMPONENT_MAP = {
    "server": serverThreadFunc,
    # "ai": aiThreadFunc,
    "display": displayThreadFunc,
}

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
    return

def startComponent(name: str, threads: dict[str, threading.Thread]):
    """Creates and starts a thread for a given component if it's not already active."""
    if name in threads and threads[name].is_alive():
        print(f"\tComponent '{name}' is already ACTIVE.")
        return

    targetFunc = COMPONENT_MAP.get(name)
    if not targetFunc:
        print(f"\t Unknown component: {name}")
        return

    try:
        newThread = threading.Thread(target=targetFunc, name=f"{name.capitalize()}Thread")
        newThread.daemon = True
        threads[name] = newThread
        newThread.start()
        print(f"\tComponent '{name}' started.")
        
    except Exception as e:
        print(f"\tError starting '{name}': {e}")


def handleRunComponent(name:str, threads: dict[str, threading.Thread]):
    componentName: str = name
    startComponent(componentName, threads)


def handleStopComponent(name: str, threads: dict[str, threading.Thread]):
    if len(name) < 1:
        print("\tSpecify component to stop (e.g., stop server).")
        return
    if name in threads and threads[name].is_alive():
        # Individual thread stopping is complex with a single STOP_EVENT.
        print(f"CMD: Individual stopping of '{name}' is not yet supported via STOP_EVENT.")
        print("Use 'quit' to stop all components.")
    else:
        print(f"\tComponent '{name}' is not active or does not exist.")


def handleStatus(threads: dict[str, threading.Thread]):
    """Displays the status of active components."""
    statusMessages: list[str] = []
    
    # Iterate through active threads dictionary
    for name, thread in threads.items():
         statusMessages.append(f"\t|{thread.name}\t| {'ACTIVE' if thread.is_alive() else 'INACTIVE'}\t|")

    cmdThread = threading.current_thread()
    statusMessages.append(f"\t|{cmdThread.name}\t| ACTIVE\t|")
    
    print("\n\t---- ACTIVE COMPONENT STATUS ----")
    print("\n".join(statusMessages))
    print("\t---------------------------------\n")



"""
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
COMMAND THREAD
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
"""
def cmdThreadFunc(threads: dict[str, threading.Thread]):
    cmdCounter = 0
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
            if fullCommand == "teapot":
                print("\tI am a Tea Pot!")
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
                    handleRunComponent(mainArg, threads)
                elif mainArg == "help":
                    print("\tUsage: run [component_name]")
                    print("\tAvailable components: " + ", ".join(COMPONENT_MAP.keys()))
                    CMD_QUEUE.put('continue')

            while CMD_QUEUE.empty() or CMD_QUEUE.get_nowait() != 'continue':
                continue
            cmdCounter += 1
            
        except EOFError:
            break
        except KeyboardInterrupt:
            break

    STOP_EVENT.set()
    print("CMD: Shutdown.")



def main():
    print("PyMania > Application started.")
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
        print("PyMania > Application terminated.")
        exit(0)


if __name__ == "__main__":
    main()