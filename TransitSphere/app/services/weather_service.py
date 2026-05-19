import os
import requests


class WeatherService:
    def current(self):
        key = os.getenv("OPENWEATHER_API_KEY", "")
        if key:
            try:
                response = requests.get(
                    "https://api.openweathermap.org/data/2.5/weather",
                    params={"q": "Bengaluru,IN", "appid": key, "units": "metric"},
                    timeout=4,
                )
                response.raise_for_status()
                data = response.json()
                return {
                    "temperature": round(data["main"]["temp"]),
                    "condition": data["weather"][0]["description"].title(),
                    "rainfall": data.get("rain", {}).get("1h", 0),
                    "impact": "Weather-aware ETAs enabled from live API",
                }
            except Exception:
                pass
        return {
            "temperature": 24,
            "condition": "Light rain risk",
            "rainfall": 1.8,
            "impact": "Demo weather model increases east-corridor delays during rainfall",
        }


weather_service = WeatherService()
