"""Motor de análise da Mission Control AI - ConnectSat."""

import os
from pathlib import Path
from textwrap import dedent

from dotenv import load_dotenv
from ollama import Client

load_dotenv()

TRILHA = "connectsat"

client = Client(
    host="https://ollama.com",
    headers={"Authorization": "Bearer " + os.environ.get("OLLAMA_API_KEY", "")},
)


def llm(prompt, system=None, max_tokens=800, temperature=0.3):
    """Envia prompt ao gpt-oss:120b via Ollama Cloud."""
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    try:
        return client.chat(
            model="gpt-oss:120b",
            messages=messages,
            options={"num_predict": max_tokens, "temperature": temperature},
            stream=False,
        )["message"]["content"].strip()
    except Exception as e:
        return f"⚠️ Erro ao consultar IA: {e}"


def load_system_prompt():
    """Lê o system prompt do projeto, com fallback seguro."""
    candidate_paths = [
        Path("prompts/systemprompt.md"),
        Path("prompts/system_prompt.md"),
    ]

    for path in candidate_paths:
        if path.exists():
            return path.read_text(encoding="utf-8")

    return (
        "Você é o analista operacional da trilha ConnectSat. "
        "Explique telemetria, alertas, risco e impacto terrestre "
        "em linguagem clara para a CLI."
    )


class MissionEngine:
    """Motor de análise da trilha ConnectSat."""

    def __init__(self):
        self.trilha = TRILHA
        self.system_prompt = load_system_prompt()
        self.last_snapshot = None
        self.last_assessment = None

        from src.telemetria import TelemetriaConnectSat
        from src.alertas import AlertManagerConnectSat

        self.telemetria = TelemetriaConnectSat()
        self.alertas = AlertManagerConnectSat()

    def is_ready(self):
        return True

    def _collect_state(self, scenario=None):
        dados = self.telemetria.coletar(scenario=scenario)
        avaliacao = self.alertas.avaliar(dados)
        self.last_snapshot = dados
        self.last_assessment = avaliacao
        return dados, avaliacao

    def _extract_scenario_hint(self, text):
        if not text:
            return None

        normalized = text.lower().strip()
        known_scenarios = [
            "nominal",
            "latencia_alta",
            "beam_degradado",
            "sobrecarga_termica",
            "crise_total",
        ]

        for scenario in known_scenarios:
            if scenario in normalized:
                return scenario
        return None

    def _risk_score(self, assessment):
        status = assessment.get("mission_status", "NORMAL")
        attention_count = assessment.get("attention_count", 0)
        critical_count = assessment.get("critical_count", 0)

        if status == "CRITICO":
            score = 75 + critical_count * 10 + attention_count * 3
        elif status == "ATENCAO":
            score = 35 + attention_count * 10
        else:
            score = 8 + attention_count * 3

        return min(score, 100)

    def _immediate_consequence(self, assessment):
        status = assessment.get("mission_status", "NORMAL")
        alerts = assessment.get("alerts", [])

        if status == "CRITICO":
            if any(alert["parametro"] == "transponder_temp_c" for alert in alerts):
                return (
                    "Risco imediato de redução forçada de capacidade do enlace, "
                    "com impacto provável em telemedicina, aulas ao vivo e acesso concorrente."
                )
            if any(alert["parametro"] == "beam_steering_error_deg" for alert in alerts):
                return (
                    "Risco imediato de intermitência ou deslocamento de cobertura sobre "
                    "a região rural atendida."
                )
            return (
                "Risco imediato de degradação severa da conectividade rural, com perda de "
                "estabilidade em serviços essenciais."
            )

        if status == "ATENCAO":
            return (
                "Há degradação perceptível no serviço; videochamadas, aulas síncronas e uso "
                "simultâneo da rede podem sofrer lentidão."
            )

        return (
            "Serviço estável no momento, sem impacto imediato relevante para a conectividade "
            "rural monitorada."
        )

    def _format_alerts(self, assessment):
        alerts = assessment.get("alerts", [])
        if not alerts:
            return "Nenhum alerta ativo."

        lines = []
        for alert in alerts:
            automated_action = (
                f" | ação: {alert['acao_automatizada']}"
                if alert.get("acao_automatizada")
                else ""
            )
            lines.append(
                f"- [{alert['severidade']}] {alert['parametro']} = {alert['valor']} {alert['unidade']} "
                f"-> {alert['mensagem']}{automated_action}"
            )
        return "\n".join(lines)

    def _format_actions(self, assessment):
        actions = assessment.get("automated_actions", [])
        if not actions:
            return "Nenhuma ação automática acionada."
        return ", ".join(actions)

    def _build_snapshot_text(self, dados, avaliacao):
        risk_score = self._risk_score(avaliacao)
        consequence = self._immediate_consequence(avaliacao)

        return dedent(
            f"""
            📡 CONNECTSAT - STATUS SNAPSHOT

            Ciclo: {dados['cycle_id']}
            Timestamp UTC: {dados['timestamp_utc']}
            Cenário simulado: {dados['scenario']}

            Parâmetros atuais
            - Latência de uplink: {dados['uplink_latency_ms']} ms
            - Throughput do feixe: {dados['beam_throughput_mbps']} Mbps
            - Saúde da antena phased-array: {dados['phased_array_health_pct']} %
            - Erro de beam steering: {dados['beam_steering_error_deg']} deg
            - Carga térmica do transponder: {dados['transponder_temp_c']} C

            Resumo operacional
            - Status da missão: {avaliacao['mission_status']}
            - Nível de risco: {risk_score}/100
            - Alertas em atenção: {avaliacao['attention_count']}
            - Alertas críticos: {avaliacao['critical_count']}

            Alertas ativos
            {self._format_alerts(avaliacao)}

            Consequência imediata no serviço
            {consequence}

            Resposta automatizada
            {self._format_actions(avaliacao)}
            """
        ).strip()

    def status_snapshot(self):
        """Retorna texto legível resumindo o estado atual da missão."""
        dados, avaliacao = self._collect_state()
        return self._build_snapshot_text(dados, avaliacao)

    def analyze(self, pergunta_usuario):
        """Analisa a pergunta com base na telemetria, alertas e IA."""
        scenario = self._extract_scenario_hint(pergunta_usuario)
        dados, avaliacao = self._collect_state(scenario=scenario)

        risk_score = self._risk_score(avaliacao)
        consequence = self._immediate_consequence(avaliacao)
        alertas_texto = self._format_alerts(avaliacao)
        acoes_texto = self._format_actions(avaliacao)
        snapshot_text = self._build_snapshot_text(dados, avaliacao)

        prompt = dedent(
            f"""
            Pergunta do operador:
            {pergunta_usuario}

            Contexto da missão:
            - trilha: ConnectSat
            - persona alvo: NOC engineer de operadora de conectividade rural

            Telemetria atual:
            - cycle_id: {dados['cycle_id']}
            - timestamp_utc: {dados['timestamp_utc']}
            - scenario: {dados['scenario']}
            - uplink_latency_ms: {dados['uplink_latency_ms']}
            - beam_throughput_mbps: {dados['beam_throughput_mbps']}
            - phased_array_health_pct: {dados['phased_array_health_pct']}
            - beam_steering_error_deg: {dados['beam_steering_error_deg']}
            - transponder_temp_c: {dados['transponder_temp_c']}

            Classificação definida em Python:
            - mission_status: {avaliacao['mission_status']}
            - risk_score: {risk_score}/100
            - attention_count: {avaliacao['attention_count']}
            - critical_count: {avaliacao['critical_count']}

            Alertas ativos:
            {alertas_texto}

            Ações automáticas já executadas:
            {acoes_texto}

            Consequência imediata no serviço:
            {consequence}

            Instruções:
            1. Não reclassifique a severidade principal; use a decisão Python como fonte de verdade.
            2. Explique a causa provável em linguagem clara.
            3. Traduza o efeito técnico para conectividade rural.
            4. Destaque impacto em escolas rurais, telemedicina e pequenos negócios quando relevante.
            5. Feche com recomendações curtas para o operador.
            6. Responda em formato legível para terminal CLI.
            """
        ).strip()

        resposta_llm = llm(
            prompt,
            system=self.system_prompt,
            max_tokens=700,
            temperature=0.2,
        )

        return dedent(
            f"""
            {snapshot_text}

            ──────────────────────────────
            🧠 ANÁLISE IA
            {resposta_llm}
            """
        ).strip()
