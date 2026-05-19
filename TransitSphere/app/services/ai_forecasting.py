import math
from datetime import datetime, timedelta


class AIForecastingService:
    def forecast(self):
        base = datetime.now().replace(minute=0, second=0, microsecond=0)
        labels = [(base + timedelta(hours=i)).strftime("%H:%M") for i in range(12)]
        demand = [int(420 + 210 * math.sin(i / 2.2) + (180 if 3 <= i <= 5 else 0) + (130 if 9 <= i <= 11 else 0)) for i in range(12)]
        congestion = [min(96, int(d / 10 + 18 + (i % 3) * 5)) for i, d in enumerate(demand)]
        return {
            "labels": labels,
            "demand": demand,
            "congestion": congestion,
            "delay_probability": [min(89, int(c * 0.72)) for c in congestion],
            "allocation": [
                {"route": "500D", "add_buses": 6, "reason": "Whitefield peak demand rising 23%"},
                {"route": "356C", "add_buses": 4, "reason": "Electronic City shift change window"},
                {"route": "335E", "add_buses": 3, "reason": "KR Puram transfer pressure"},
            ],
        }

    def insights(self):
        return [
            "LSTM model predicts east corridor overcrowding between 18:00 and 20:00.",
            "Rain-sensitive delay model recommends 8 extra buses on ORR and Whitefield routes.",
            "Silk Board bottleneck probability is high; reroute express services via Hosur Road bypass.",
        ]


forecast_service = AIForecastingService()
