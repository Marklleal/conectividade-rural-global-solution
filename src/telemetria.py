# src/telemetria.py
from __future__ import annotations

import random
from datetime import datetime
from typing import Dict, Optional


class TelemetriaConnectSat:
    """
    Gera snapshots simulados da missão ConnectSat.
    Cada ciclo representa uma leitura operacional resumida do satélite.
    """

    def __init__(self, seed: Optional[int] = None):
        self.random = random.Random(seed)
        self.cycle_id = 0

    def _clamp(self, value: float, low: float, high: float) -> float:
        return max(low, min(value, high))

    def _sample_nominal(self) -> Dict[str, float]:
        return {
            "uplink_latency_ms": round(self.random.uniform(18, 45), 2),
            "beam_throughput_mbps": round(self.random.uniform(120, 220), 2),
            "phased_array_health_pct": round(self.random.uniform(92, 100), 2),
            "beam_steering_error_deg": round(self.random.uniform(0.00, 0.25), 3),
            "transponder_temp_c": round(self.random.uniform(45, 72), 2),
        }

    def _apply_scenario(self, base: Dict[str, float], scenario: str) -> Dict[str, float]:
        data = dict(base)

        if scenario == "nominal":
            return data

        if scenario == "latencia_alta":
            data["uplink_latency_ms"] = round(self.random.uniform(70, 120), 2)
            data["beam_throughput_mbps"] = round(self.random.uniform(85, 140), 2)

        elif scenario == "beam_degradado":
            data["phased_array_health_pct"] = round(self.random.uniform(58, 84), 2)
            data["beam_steering_error_deg"] = round(self.random.uniform(0.45, 1.40), 3)
            data["beam_throughput_mbps"] = round(self.random.uniform(55, 125), 2)

        elif scenario == "sobrecarga_termica":
            data["transponder_temp_c"] = round(self.random.uniform(78, 96), 2)
            data["beam_throughput_mbps"] = round(self.random.uniform(60, 130), 2)
            data["uplink_latency_ms"] = round(self.random.uniform(35, 85), 2)

        elif scenario == "crise_total":
            data["uplink_latency_ms"] = round(self.random.uniform(95, 180), 2)
            data["beam_throughput_mbps"] = round(self.random.uniform(25, 85), 2)
            data["phased_array_health_pct"] = round(self.random.uniform(40, 74), 2)
            data["beam_steering_error_deg"] = round(self.random.uniform(0.90, 2.20), 3)
            data["transponder_temp_c"] = round(self.random.uniform(86, 110), 2)

        return data

    def coletar(self, scenario: Optional[str] = None) -> Dict:
        """
        Retorna um snapshot de telemetria.
        Se scenario=None, escolhe automaticamente com predominância nominal.
        """
        self.cycle_id += 1

        if scenario is None:
            scenario = self.random.choices(
                population=[
                    "nominal",
                    "latencia_alta",
                    "beam_degradado",
                    "sobrecarga_termica",
                    "crise_total",
                ],
                weights=[60, 15, 12, 10, 3],
                k=1,
            )[0]

        base = self._sample_nominal()
        payload = self._apply_scenario(base, scenario)

        payload["cycle_id"] = self.cycle_id
        payload["scenario"] = scenario
        payload["timestamp_utc"] = datetime.utcnow().isoformat() + "Z"

        return payload
