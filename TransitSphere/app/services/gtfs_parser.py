import csv
import os
from flask import current_app


class GTFSParser:
    def __init__(self):
        self._cache = {}

    def _base(self):
        try:
            return current_app.config["GTFS_PATH"]
        except RuntimeError:
            return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "gtfs"))

    def _read(self, name):
        if name in self._cache:
            return self._cache[name]
        path = os.path.join(self._base(), name)
        with open(path, newline="", encoding="utf-8-sig") as handle:
            rows = list(csv.DictReader(handle))
        self._cache[name] = rows
        return rows

    def routes(self):
        if "routes_enriched" not in self._cache:
            palette = ["38BDF8", "34D399", "FBBF24", "FB7185", "A78BFA", "22C55E", "F97316", "60A5FA"]
            enriched = []
            for index, row in enumerate(self._read("routes.txt")):
                item = dict(row)
                item.setdefault("route_color", palette[index % len(palette)])
                item.setdefault("route_text_color", "07111E")
                if not item.get("route_color"):
                    item["route_color"] = palette[index % len(palette)]
                if not item.get("route_text_color"):
                    item["route_text_color"] = "07111E"
                enriched.append(item)
            self._cache["routes_enriched"] = enriched
        return self._cache["routes_enriched"]

    def featured_routes(self, limit=18):
        keywords = ["KBS", "Majestic", "Shivajinagara", "Whitefield", "Electronic", "Hebbal", "KR Puram", "Banashankari", "Silk"]
        scored = []
        for route in self.routes():
            name = f"{route.get('route_short_name', '')} {route.get('route_long_name', '')}"
            score = sum(1 for word in keywords if word.lower() in name.lower())
            if score:
                scored.append((score, route))
        selected = [route for _, route in sorted(scored, key=lambda item: (-item[0], item[1].get("route_short_name", "")))[:limit]]
        if len(selected) < limit:
            seen = {route["route_id"] for route in selected}
            selected.extend([route for route in self.routes() if route["route_id"] not in seen][: limit - len(selected)])
        return selected

    def stops(self):
        return [
            {
                "stop_id": row["stop_id"],
                "stop_name": row["stop_name"],
                "lat": float(row["stop_lat"]),
                "lng": float(row["stop_lon"]),
                "density": int(row.get("density", 40) or 40),
            }
            for row in self._read("stops.txt")
        ]

    def stops_by_id(self):
        if "stops_by_id" not in self._cache:
            self._cache["stops_by_id"] = {stop["stop_id"]: stop for stop in self.stops()}
        return self._cache["stops_by_id"]

    def trips(self):
        return self._read("trips.txt")

    def trips_by_route(self):
        if "trips_by_route" not in self._cache:
            grouped = {}
            for trip in self.trips():
                grouped.setdefault(trip["route_id"], []).append(trip)
            self._cache["trips_by_route"] = grouped
        return self._cache["trips_by_route"]

    def shape_points(self, shape_id, max_points=160):
        cache_key = f"shape:{shape_id}:{max_points}"
        if cache_key in self._cache:
            return self._cache[cache_key]
        points = []
        path = os.path.join(self._base(), "shapes.txt")
        with open(path, newline="", encoding="utf-8-sig") as handle:
            for row in csv.DictReader(handle):
                if row.get("shape_id") == shape_id:
                    points.append(row)
        ordered = sorted(points, key=lambda p: int(float(p.get("shape_pt_sequence", 0))))
        if len(ordered) > max_points:
            step = max(1, len(ordered) // max_points)
            ordered = ordered[::step][:max_points]
        shape = [[float(point["shape_pt_lat"]), float(point["shape_pt_lon"])] for point in ordered]
        self._cache[cache_key] = shape
        return shape

    def stop_times_for_trip(self, trip_id):
        cache_key = f"stop_times:{trip_id}"
        if cache_key in self._cache:
            return self._cache[cache_key]
        rows = []
        path = os.path.join(self._base(), "stop_times.txt")
        with open(path, newline="", encoding="utf-8-sig") as handle:
            for row in csv.DictReader(handle):
                if row.get("trip_id") == trip_id:
                    rows.append(row)
        rows = sorted(rows, key=lambda s: int(float(s.get("stop_sequence", 0))))
        self._cache[cache_key] = rows
        return rows

    def featured_details(self, limit=18):
        cache_key = f"featured_details:{limit}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        routes = self.featured_routes(limit)
        trips_by_route = self.trips_by_route()
        route_trips = {
            route["route_id"]: trips_by_route.get(route["route_id"], [self.trips()[0]])[0]
            for route in routes
        }
        trip_ids = {trip["trip_id"] for trip in route_trips.values()}
        stop_times = {trip_id: [] for trip_id in trip_ids}
        with open(os.path.join(self._base(), "stop_times.txt"), newline="", encoding="utf-8-sig") as handle:
            for row in csv.DictReader(handle):
                trip_id = row.get("trip_id")
                if trip_id in stop_times:
                    stop_times[trip_id].append(row)

        stops_by_id = self.stops_by_id()
        details = {}
        for route in routes:
            trip = route_trips[route["route_id"]]
            times = sorted(stop_times.get(trip["trip_id"], []), key=lambda s: int(float(s.get("stop_sequence", 0))))
            stops = [stops_by_id[st["stop_id"]] for st in times if st.get("stop_id") in stops_by_id]
            details[route["route_id"]] = {
                "route": route,
                "trip": trip,
                "shape": [[stop["lat"], stop["lng"]] for stop in stops],
                "stops": stops,
            }
        self._cache[cache_key] = details
        return details

    def route_detail(self, route_id):
        featured = self.featured_details(18)
        if route_id in featured:
            return featured[route_id]
        route = next((r for r in self.routes() if r["route_id"] == route_id), self.routes()[0])
        trip = self.trips_by_route().get(route["route_id"], self.trips())[0]
        stop_times = self.stop_times_for_trip(trip["trip_id"])
        stops_by_id = self.stops_by_id()
        stops = [stops_by_id[st["stop_id"]] for st in stop_times if st["stop_id"] in stops_by_id]
        shape = [[stop["lat"], stop["lng"]] for stop in stops]
        return {
            "route": route,
            "trip": trip,
            "shape": shape,
            "stops": stops,
        }


gtfs = GTFSParser()
