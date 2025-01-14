import requests
import datetime
import time

@staticmethod
def get_weather_info(api_key, lat, lon):
  """
  Fetch weather information for a given latitude and longitude.
  Extract specific details: weather main and description, temperature, wind speed, city name, and country.
  """
  base_url = "https://api.openweathermap.org/data/2.5/weather"
  params = {
    "lat": lat,
    "lon": lon,
    "appid": api_key,
    "units": "imperial"  # Get temperature in Fahrenheit
  }

  try:
    response = requests.get(base_url, params=params)
    response.raise_for_status()  # Raise exception for HTTP errors
    data = response.json()

    # Extract the required details
    weather = data.get("weather", [{}])[0]
    main = data.get("main", {})
    wind = data.get("wind", {})
    timezone = data.get("timezone", "N/A")
    time = calculate_local_time(timezone)
    # Format the result as a string
    result = (
      f"Weather: {weather.get('main', 'N/A').lower()} - {weather.get('description', 'N/A').lower()}\n"
      f"Temperature: {main.get('temp', 'N/A')}°F, Feels like: {main.get('feels_like', 'N/A')}°F\n"
      f"Wind Speed: {wind.get('speed', 'N/A')} mph\n"
      f"City: {data.get('name', 'N/A')}, {data.get('sys', {}).get('country', 'N/A')}\n"
      f"Current Time: {time}"
    )
    return result
  except requests.RequestException as e:
    return f"Request failed: {e}"

@staticmethod
def calculate_local_time(target_timezone_offset: int) -> str:
  """
  Calculate the local time in a target timezone using the user's system time.
  
  :param target_timezone_offset: The target timezone offset (in seconds) from OpenWeatherMap data.
  :return: The local time in the target timezone as a string.
  """
  # Step 1: Get the user's current timezone offset in seconds
  user_timezone_offset = -time.timezone
  if time.localtime().tm_isdst:
      user_timezone_offset += time.altzone - time.timezone

  # Step 2: Get the current system time in UTC
  #now_utc = datetime.datetime.utcnow()
  now_utc = datetime.datetime.now(datetime.timezone.utc)

  # Step 3: Adjust the UTC time by the difference between user and target timezone
  # (target offset - user offset gives the adjustment needed)
  adjustment_seconds = target_timezone_offset - user_timezone_offset
  target_time = now_utc + datetime.timedelta(seconds=adjustment_seconds)

  # Return the local time in the target timezone
  return target_time.strftime('%Y-%m-%d %H:%M:%S')