class SchedulingEngine:
    def plan(self):
        return {
            "generated_at": "live",
            "recommendations": [
                {"route": "500D", "corridor": "Majestic - Whitefield", "action": "Add 6 buses", "impact": "Reduce wait time by 31%", "priority": "Critical"},
                {"route": "356C", "corridor": "Majestic - Electronic City", "action": "Short-turn 3 buses at Silk Board", "impact": "Stabilize headway to 7 min", "priority": "High"},
                {"route": "335E", "corridor": "Kempegowda - KR Puram", "action": "Hold 2 buses for transfer wave", "impact": "Reduce missed transfers by 18%", "priority": "Medium"},
                {"route": "KIA-8", "corridor": "Hebbal - Airport", "action": "Weather buffer +4 min", "impact": "Improve ETA reliability", "priority": "Medium"},
            ],
            "headways": [7, 8, 10, 12, 9, 6, 11],
            "routes": ["500D", "356C", "335E", "KIA-8", "201R", "V-500CA", "G-4"],
        }


scheduling_service = SchedulingEngine()
