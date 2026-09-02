from dataclasses import dataclass, field
from typing import Callable
from PyQt6.QtWidgets import QApplication
import time
import numpy as np

from pmpk.store import Store
from pmpk.geometry import drawHelicoidaleCurve, drawRandomCurve, recenterDataFrame
from pmpk.store import Context




@dataclass
class Command:
    name: str
    func: Callable[[list[str], Context], str|None]
    help: str = "No description given."
    format: str = "No format given."
    aliases: list[str] = field(default_factory=list)

class CommandRegistry:
    def __init__(self) -> None:
        self._commands: dict[str, Command] = {}
    
    def register(self, name: str, help: str = "No description given.", format: str = "No format given.", aliases: list[str] = []):
        def wrapper(func: Callable[[list[str], Context], str | None]):
            cmd = Command(name=name, func=func, help=help, format=format, aliases=aliases)
            self._commands[name] = cmd
            for alias in aliases:
                self._commands[alias] = cmd
            return func
        return wrapper
    
    def execute(self, raw_input: str, context: Context) -> str:
        parts = raw_input.strip().split()
        if not parts:
            return ""
        name, args = parts[0].lower(), parts[1:]

        command = self._commands.get(name)
        if command is None:
            return f"Error : Command '{name}' not found."

        try:
            result = command.func(args, context)
            return result or ""
        except Exception as e:
            return f"Execution Error : {e}"
        
    def getCommandsHelp(self):
        s = ""
        seen: set[str] = set() 
        for command in self._commands.values():
            if command.name in seen:
                continue
            seen.add(command.name)
            
            aliases_str = f"[alias: {', '.join(command.aliases)}]\n\t" if command.aliases else ""
            s += f"{command.name}\t{command.help}\n\t{aliases_str}{command.format}\n"
        return s
    
    def getCommandHelp(self, name: str):
        command = self._commands.get(name)
        if command is None:
            return f"Error : Command '{name}' not found."
            
        aliases_str = f"[alias: {', '.join(command.aliases)}]\n\t" if command.aliases else ""
        return f"{command.name}\t{command.help}\n\t{aliases_str}{command.format}"
    

def build_registry() -> CommandRegistry:
    registry = CommandRegistry()
    
    @registry.register("help", help="Get command list and details.", format="`help <_|command_name>`")
    def help(args: list[str], context: Context):
        if len(args) == 0:
            context.log(registry.getCommandsHelp())
        else: context.log(registry.getCommandHelp(args[0]))

    @registry.register("ping", help="Check console's base answer time.", format="`ping`")
    def ping(args: list[str], context: Context) -> str:
        sent_at = context.ts
        elapsed_ms = (time.perf_counter() - sent_at) * 1000
        context.log("test")
        return f"Console answered in {elapsed_ms:.2f} ms"
    
    @registry.register("clear", help="Clear console's output and history", format="`clear`")
    def clear(args:list[str], context: Context):
        return "__CLEAR__"
    
    @registry.register("draw", help="Draw curve based on a function or a file.", format="`draw <function or file> <function params> <axis to center around>`")
    def draw(args:list[str], context: Context):
        win_g = Store().getState("win_g")
        axis = {"x", "y", "z"}
        centering_axis = list(axis) if "c" in args else list(set([e for e in args if e in axis]))
        cleaned_args = [e for e in args if e not in axis and e != "c"]
        match cleaned_args[0]:
            case "curve":
                df  = drawHelicoidaleCurve(ppl=50, n_layers=4, z_dif=4)
            case "random":
                df = drawRandomCurve(n_points=400)
            case "clear":
                df = np.empty((0, 3))
            case _ :
                df = None
        if len(centering_axis) : context.log(f"Centering DataFrame on axis {", ".join(centering_axis)}")
        df = recenterDataFrame(df, centering_axis) # type: ignore
        context.log("Setting 3DLine as per ordered.")
        win_g.setLine(pos=df, color=(0, 1, 0, 1)) # type: ignore
        return
    
    
    @registry.register("close", help="Closes the App", format="`close`", aliases=["exit"])
    def close(args:list[str], context: Context):
        QApplication.instance().quit() # type: ignore
    
            
    
    return registry

