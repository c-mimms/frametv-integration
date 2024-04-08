import requests

def get_forecast():
    # Get the weather forecast for the next 3 days
    latitude = "33.7431791"
    longitude = "-84.3525177"
    response = requests.get("https://api.open-meteo.com/v1/forecast?latitude=33.743&longitude=-84.352&daily=weather_code,temperature_2m_max,temperature_2m_min,sunrise,sunset,uv_index_max,precipitation_sum,rain_sum,showers_sum,precipitation_hours,precipitation_probability_max,wind_speed_10m_max&temperature_unit=fahrenheit&wind_speed_unit=kn&precipitation_unit=inch&timezone=America%2FNew_York&forecast_days=3")
    forecast = response.json()
    

    return parse_forecast(forecast)

def parse_forecast(forecast):

    parsed_forecast = []
    for i in range(3):
        day = forecast['daily']['time'][i]
        weather_code = forecast['daily']['weather_code'][i]
        max_temp = forecast['daily']['temperature_2m_max'][i]
        min_temp = forecast['daily']['temperature_2m_min'][i]
        sunrise = forecast['daily']['sunrise'][i]
        sunset = forecast['daily']['sunset'][i]
        uv_index = forecast['daily']['uv_index_max'][i]
        precipitation = forecast['daily']['precipitation_sum'][i]
        rain = forecast['daily']['rain_sum'][i]
        showers = forecast['daily']['showers_sum'][i]
        precipitation_hours = forecast['daily']['precipitation_hours'][i]
        precipitation_probability = forecast['daily']['precipitation_probability_max'][i]
        wind_speed = forecast['daily']['wind_speed_10m_max'][i]
        parsed_forecast.append({
            'day': day,
            'weather_code': weather_code,
            'max_temp': max_temp,
            'min_temp': min_temp,
            'sunrise': sunrise,
            'sunset': sunset,
            'uv_index': uv_index,
            'precipitation': precipitation,
            'rain': rain,
            'showers': showers,
            'precipitation_hours': precipitation_hours,
            'precipitation_probability': precipitation_probability,
            'wind_speed': wind_speed
        })
    return parsed_forecast

# def main():
#     forecast = get_forecast()
#     parsed_forecast = parse_forecast(forecast)
#     #Print high temp each day
#     for day in parsed_forecast:
#         print(f"High temp for {day['day']}: {day['max_temp']}")

# if __name__ == "__main__":
#     main()

# Format :
# 'day': day,
# 'weather_code': weather_code,
# 'max_temp': max_temp,
# 'min_temp': min_temp,
# 'sunrise': sunrise,
# 'sunset': sunset,
# 'uv_index': uv_index,
# 'precipitation': precipitation,
# 'rain': rain,
# 'showers': showers,
# 'precipitation_hours': precipitation_hours,
# 'precipitation_probability': precipitation_probability,
# 'wind_speed': wind_speed

# Weather codes
# Code 	Description
# 0 	Clear sky
# 1, 2, 3 	Mainly clear, partly cloudy, and overcast
# 45, 48 	Fog and depositing rime fog
# 51, 53, 55 	Drizzle: Light, moderate, and dense intensity
# 56, 57 	Freezing Drizzle: Light and dense intensity
# 61, 63, 65 	Rain: Slight, moderate and heavy intensity
# 66, 67 	Freezing Rain: Light and heavy intensity
# 71, 73, 75 	Snow fall: Slight, moderate, and heavy intensity
# 77 	Snow grains
# 80, 81, 82 	Rain showers: Slight, moderate, and violent
# 85, 86 	Snow showers slight and heavy
# 95 * 	Thunderstorm: Slight or moderate
# 96, 99 * 	Thunderstorm with slight and heavy hail