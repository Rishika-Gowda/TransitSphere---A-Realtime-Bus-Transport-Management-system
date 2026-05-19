import math
import random
import time
from app.services.gtfs_parser import gtfs


class SimulationEngine:
    def __init__(self):
        self.started = time.time()
        self.fleet = []

    def _seed(self):
        if self.fleet:
            return
        names = ["KA-57-F-1201", "KA-57-F-1348", "KA-01-F-8832", "KA-53-F-4421", "KA-05-F-7902", "KA-41-F-6620", "KA-51-F-2918", "KA-03-F-7712"]
        statuses = ["On Time", "Delayed", "Congested", "On Time", "On Time", "Maintenance"]
        for index, route in enumerate(gtfs.featured_routes(18)):
            detail = gtfs.route_detail(route["route_id"])
            fallback_shape = [
                [12.9767 + (index % 6) * 0.012, 77.5713 + (index % 5) * 0.018],
                [12.9450 + (index % 4) * 0.015, 77.6100 + (index % 6) * 0.021],
                [12.9700 + (index % 5) * 0.011, 77.6800 + (index % 4) * 0.018],
            ]
            self.fleet.append({
                "bus_id": names[index % len(names)],
                "route_id": route["route_id"],
                "route_name": route["route_short_name"],
                "status": statuses[index % len(statuses)],
                "shape": detail["shape"] or fallback_shape,
                "stops": detail["stops"],
                "phase": index * 0.14,
                "occupancy": 48 + index * 7,
                "delay": index % 4,
                "speed": 28 + index * 3,
            })

    def _position(self, bus, now):
        shape = bus["shape"]
        if not shape:
            return [12.9763, 77.5929]
        progress = (bus["phase"] + (now - self.started) / 180.0) % 1
        raw = progress * (len(shape) - 1)
        left = int(math.floor(raw))
        right = min(left + 1, len(shape) - 1)
        t = raw - left
        lat = shape[left][0] + (shape[right][0] - shape[left][0]) * t
        lng = shape[left][1] + (shape[right][1] - shape[left][1]) * t
        return [round(lat, 6), round(lng, 6)]

    def tick(self):
        self._seed()
        now = time.time()
        buses = []
        for bus in self.fleet:
            wave = math.sin(now / 18 + bus["phase"] * 9)
            occupancy = max(12, min(98, int(bus["occupancy"] + wave * 18 + random.randint(-3, 3))))
            status = "Congested" if occupancy > 86 else ("Delayed" if bus["delay"] > 5 else bus["status"])
            speed = max(8, int(bus["speed"] + wave * 8 - (occupancy > 85) * 7))
            next_stop = bus["stops"][int((now / 45 + bus["phase"] * 10) % len(bus["stops"]))]["stop_name"] if bus["stops"] else "Terminal"
            buses.append({
                "bus_id": bus["bus_id"],
                "route_id": bus["route_id"],
                "route_name": bus["route_name"],
                "lat": self._position(bus, now)[0],
                "lng": self._position(bus, now)[1],
                "occupancy": occupancy,
                "delay": max(0, int(bus["delay"] + (occupancy - 70) / 12)),
                "speed": speed,
                "status": status,
                "next_stop": next_stop,
            })
        return {"timestamp": int(now), "buses": buses, "kpis": self.kpis(buses)}

    def snapshot(self):
        return self.tick()["buses"]

    def kpis(self, buses=None):
        buses = buses or self.snapshot() if hasattr(self, "fleet") and self.fleet else []
        avg_occ = int(sum(b["occupancy"] for b in buses) / max(1, len(buses)))
        delayed = sum(1 for b in buses if b["delay"] > 3 or b["status"] == "Delayed")
        return {
            "active_buses": len(buses),
            "total_routes": len(gtfs.routes()),
            "live_occupancy": avg_occ,
            "congestion_index": min(98, 42 + delayed * 8 + max(0, avg_occ - 65)),
            "delayed_buses": delayed,
            "predicted_demand": 7420 + avg_occ * 18,
            "fuel_efficiency": round(4.8 - delayed * 0.12, 1),
            "route_performance": max(62, 94 - delayed * 6),
        }


simulator = SimulationEngine()
