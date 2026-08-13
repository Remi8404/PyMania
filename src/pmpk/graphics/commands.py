from dataclasses import dataclass
from typing import Callable, Any
import time


@dataclass
class Command:
    func: Callable[[list[str], dict[str, Any]], str|None]
    help: str = "No description given."

class CommandRegistry:
    def __init__(self) -> None:
        self._commands: dict[str, Command] = {}
    
    def register(self, name: str, help: str = "No description given."):
        def wrapper(func: Callable[[list[str], dict[str, Any]], str | None]):
            self._commands[name] = Command(func=func, help=help)
            return func
        return wrapper
    
    def execute(self, raw_input: str, context: dict[str, Any]) -> str:
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
    

def build_registry() -> CommandRegistry:
    registry = CommandRegistry()

    @registry.register("ping", help="Check console's base answer time.")
    def ping(args: list[str], context: dict[str, Any]) -> str:
        sent_at = context["timestamp"]
        elapsed_ms = (time.perf_counter() - sent_at) * 1000
        context["log"]("test") #change this to an object as context.log("test")
        return f"Console answered in {elapsed_ms:.2f} ms"
    
    @registry.register("clear", help="Clear console's output and history")
    def clear(args:list[str], context: dict[str, Any]):
        return "__CLEAR__"
    
    return registry

