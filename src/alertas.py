# src/alertas.py
from __future__ import annotations

from typing import Dict, List


NORMAL = "NORMAL"
ATENCAO = "ATENCAO"
CRITICO = "CRITICO"


class AlertManagerConnectSat:
    def __init__(self):
        self.thresholds = {
            "uplink_latency_ms": {
                "unit": "ms",
                "attention_min": 45,
                "critical_min": 80,
            },
            "beam_throughput_mbps": {
                "unit": "Mbps",
                "attention_max": 120,
                "critical_max": 80,
            },
            "phased_array_health_pct": {
                "unit": "%",
                "attention_max": 92,
                "critical_max": 75,
            },
            "beam_steering_error_deg": {
                "unit": "deg",
                "attention_min": 0.25,
                "critical_min": 0.80,
            },
            "transponder_temp_c": {
                "unit": "C",
                "attention_min": 72,
                "critical_min": 85,
            },
        }

    def _severity_latency(self, value: float) -> str:
        if value > self.thresholds["uplink_latency_ms"]["critical_min"]:
            return CRITICO
        if value > self.thresholds["uplink_latency_ms"]["attention_min"]:
            return ATENCAO
        return NORMAL

    def _severity_throughput(self, value: float) -> str:
        if value < self.thresholds["beam_throughput_mbps"]["critical_max"]:
            return CRITICO
        if value < self.thresholds["beam_throughput_mbps"]["attention_max"]:
            return ATENCAO
        return NORMAL

    def _severity_health(self, value: float) -> str:
        if value < self.thresholds["phased_array_health_pct"]["critical_max"]:
            return CRITICO
        if value < self.thresholds["phased_array_health_pct"]["attention_max"]:
            return ATENCAO
        return NORMAL

    def _severity_steering(self, value: float) -> str:
        if value > self.thresholds["beam_steering_error_deg"]["critical_min"]:
            return CRITICO
        if value > self.thresholds["beam_steering_error_deg"]["attention_min"]:
            return ATENCAO
        return NORMAL

    def _severity_temp(self, value: float) -> str:
        if value > self.thresholds["transponder_temp_c"]["critical_min"]:
            return CRITICO
        if value > self.thresholds["transponder_temp_c"]["attention_min"]:
            return ATENCAO
        return NORMAL

    def _make_alert(
        self,
        parametro: str,
        valor: float,
        unidade: str,
        severidade: str,
        mensagem: str,
        impacto_servico: str,
        acao_automatizada: str | None = None,
    ) -> Dict:
        return {
            "parametro": parametro,
            "valor": valor,
            "unidade": unidade,
            "severidade": severidade,
            "mensagem": mensagem,
            "impacto_servico": impacto_servico,
            "acao_automatizada": acao_automatizada,
        }

    def avaliar(self, telemetria: Dict) -> Dict:
        alerts: List[Dict] = []

        latency = telemetria["uplink_latency_ms"]
        throughput = telemetria["beam_throughput_mbps"]
        health = telemetria["phased_array_health_pct"]
        steering = telemetria["beam_steering_error_deg"]
        temp = telemetria["transponder_temp_c"]

        sev_latency = self._severity_latency(latency)
        sev_throughput = self._severity_throughput(throughput)
        sev_health = self._severity_health(health)
        sev_steering = self._severity_steering(steering)
        sev_temp = self._severity_temp(temp)

        if sev_latency != NORMAL:
            alerts.append(
                self._make_alert(
                    "uplink_latency_ms",
                    latency,
                    "ms",
                    sev_latency,
                    "Latência de uplink acima do esperado para operação estável.",
                    "Pode degradar aplicações interativas como aula síncrona, voz e teleconsulta.",
                )
            )

        if sev_throughput != NORMAL:
            alerts.append(
                self._make_alert(
                    "beam_throughput_mbps",
                    throughput,
                    "Mbps",
                    sev_throughput,
                    "Throughput do feixe abaixo da capacidade operacional desejada.",
                    "Pode reduzir qualidade de vídeo, uploads e acesso simultâneo da comunidade atendida.",
                )
            )

        if sev_health != NORMAL:
            alerts.append(
                self._make_alert(
                    "phased_array_health_pct",
                    health,
                    "%",
                    sev_health,
                    "Saúde da antena phased-array abaixo do patamar ideal.",
                    "Pode afetar estabilidade e formação do feixe sobre a área de cobertura.",
                )
            )

        if sev_steering != NORMAL:
            alerts.append(
                self._make_alert(
                    "beam_steering_error_deg",
                    steering,
                    "deg",
                    sev_steering,
                    "Erro de beam steering acima do aceitável.",
                    "Pode deslocar o feixe da região atendida e gerar intermitência de conexão.",
                )
            )

        if sev_temp != NORMAL:
            action = None
            if sev_temp == CRITICO:
                action = "ATIVAR_THERMAL_PROTECTION_MODE"
            alerts.append(
                self._make_alert(
                    "transponder_temp_c",
                    temp,
                    "C",
                    sev_temp,
                    "Carga térmica do transponder acima do limite seguro.",
                    "Risco de degradação do enlace, throttling e perda parcial de capacidade.",
                    acao_automatizada=action,
                )
            )

        attention_count = sum(
            1 for s in [sev_latency, sev_throughput, sev_health, sev_steering, sev_temp] if s == ATENCAO
        )
        critical_count = sum(
            1 for s in [sev_latency, sev_throughput, sev_health, sev_steering, sev_temp] if s == CRITICO
        )

        mission_status = NORMAL
        automated_actions: List[str] = []

        if critical_count >= 1:
            mission_status = CRITICO
        elif attention_count >= 1:
            mission_status = ATENCAO

        # Escalonamento por correlação
        if sev_steering == CRITICO and sev_health in [ATENCAO, CRITICO]:
            mission_status = CRITICO
            automated_actions.append("REORIENTAR_FEIXE_E_PRIORIZAR_ESTABILIDADE")

        if sev_temp == CRITICO:
            mission_status = CRITICO
            automated_actions.append("REDUZIR_CARGA_DO_TRANSPONDER")
            automated_actions.append("NOTIFICAR_NOC_IMEDIATAMENTE")

        if sev_latency == CRITICO and sev_throughput == CRITICO:
            mission_status = CRITICO
            automated_actions.append("REALOCAR_CAPACIDADE_PARA_SERVICOS_ESSENCIAIS")

        summary = {
            "mission_status": mission_status,
            "attention_count": attention_count,
            "critical_count": critical_count,
            "alerts": alerts,
            "automated_actions": list(dict.fromkeys(automated_actions)),
        }

        return summary
