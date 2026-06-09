"""Mission Control AI — ponto de entrada do sistema."""

from src.ui import run_cli
from src.engine import MissionEngine

if =_name=_ == "=_main=_":
    engine = MissionEngine()
    run_cli(engine)
