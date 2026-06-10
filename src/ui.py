"""Interface CLI estilo Claude Code — usa Rich + prompt-toolkit."""
import subprocess
import sys
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style
import pyfiglet
from datetime import datetime

console = Console()
session = PromptSession(style=Style.from_dict({"prompt": "#06B6D4 bold"}))

def show_banner():
    """Exibe banner ASCII executando o script externo no início."""
    # Caminho mais confiável: sempre relativo à raiz do projeto
    project_root = Path(__file__).parent.parent  # sobe de src/ para a raiz
    script_path = project_root / "banner_ascii.py"

    try:
        if not script_path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {script_path}")

        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            check=True,
            cwd=project_root  # garante que o script rode na raiz do projeto
        )
        banner_output = result.stdout
    except Exception as e:  # captura qualquer erro de forma mais clara
        banner_output = f"[Erro ao carregar o banner externo: {e}]"

    console.print(Text(banner_output, style="bold #06B6D4"))

    # Painel inferior
    console.print(Panel.fit(
        "Sistema de monitoramento e análise por IA generativa.\n"
        "Use /help para ver os comandos · /exit para sair.\n"
        "Modelo: gpt-oss:120b via Ollama Cloud",
        title="◆ MISSION CONTROL",
        border_style="#06B6D4"
    ))

def show_response(text):
    """Renderiza resposta da IA em painel com timestamp."""
    now = datetime.now().strftime("%H:%M")
    console.print(Panel(text, title="◆ Mission Control",
                        subtitle=now, border_style="#06B6D4"))

def run_cli(engine):
    """Loop principal da CLI."""
    show_banner()
    if not engine.is_ready():
        console.print(" ⚠ Engine status: AGUARDANDO IMPLEMENTAÇÃO ✗\n", style="yellow")

    while True:
        try:
            user_input = session.prompt("❯ ").strip()
        except (KeyboardInterrupt, EOFError):
            break
        if not user_input:
            continue
        if user_input == "/exit":
            break
        if user_input == "/help":
            console.print("Comandos: /help /status /about /clear /exit")
            continue
        if user_input == "/status":
            show_response(engine.status_snapshot())
            continue
        if user_input == "/about":
            show_response(
                "📡 ConnectSat\n\n"
                "Trilha focada em conectividade rural via satélite LEO.\n"
                "Monitora latência, throughput, saúde da antena, beam steering\n"
                "e carga térmica do transponder.\n\n"
                "Persona principal: NOC engineer.\n"
                "Impacto terrestre: escolas rurais, telemedicina e pequenos negócios sem fibra."
            )
            continue
        if user_input == "/clear":
            console.clear(); show_banner(); continue# Qualquer outra entrada vai para o motor de análise
        resposta = engine.analyze(user_input)
        show_response(resposta)
