class CongestionEngine:
    def hotspots(self):
        return [
            {"name": "Silk Board Junction", "lat": 12.9177, "lng": 77.6238, "intensity": 0.94, "delay": 18},
            {"name": "KR Puram Bridge", "lat": 13.0006, "lng": 77.6760, "intensity": 0.78, "delay": 13},
            {"name": "Hebbal Flyover", "lat": 13.0358, "lng": 77.5970, "intensity": 0.71, "delay": 11},
            {"name": "Majestic Terminal", "lat": 12.9767, "lng": 77.5713, "intensity": 0.67, "delay": 9},
            {"name": "Whitefield Main Road", "lat": 12.9698, "lng": 77.7499, "intensity": 0.82, "delay": 15},
            {"name": "Electronic City Phase 1", "lat": 12.8452, "lng": 77.6602, "intensity": 0.74, "delay": 12},
        ]

    def alerts(self):
        return [
            {"priority": "Critical", "title": "Heavy congestion at Silk Board", "body": "Average route delay is 18 minutes. Dispatch express relief buses.", "tag": "Congestion"},
            {"priority": "High", "title": "Overcrowding on 500D", "body": "Live occupancy crossed 91% near Marathahalli.", "tag": "Demand"},
            {"priority": "Medium", "title": "Rain cell approaching East Bengaluru", "body": "Weather-aware ETA model increased delays for Whitefield routes.", "tag": "Weather"},
            {"priority": "Low", "title": "Preventive maintenance window", "body": "Two buses due for inspection after evening peak.", "tag": "Maintenance"},
        ]


congestion_service = CongestionEngine()
