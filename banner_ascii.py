import pyfiglet
from rich.console import Console
from rich.align import Align
from rich.text import Text

console = Console()

linha1 = pyfiglet.figlet_format("Global Solution", font="ansi_shadow")
linha2 = pyfiglet.figlet_format("Mission Control AI", font="ansi_shadow")
linha3 = pyfiglet.figlet_format("ConnectSat", font="small")

console.print(Align.center(Text(linha1, style="bold #A855F7")))
console.print(Align.center(Text(linha2, style="bold #06B6D4")))
console.print(Align.center(Text(linha3, style="bold #22C55E")))
console.print(
    Align.center(
        Text(
            "── 2026.1 · ConnectSat · Rural Connectivity Mission ──",
            style="italic #8484A0",
        )
    )
)
