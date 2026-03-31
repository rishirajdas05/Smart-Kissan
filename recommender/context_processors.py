def nav_context(request):
    """
    Global navbar context:
    - weather pill value
    - current language
    - auth links
    """
    # Weather shown in navbar (you can replace with real API later)
    nav_weather_temp = request.session.get("nav_weather_temp", "10.0")

    return {
        "nav_weather_temp": nav_weather_temp,
    }
