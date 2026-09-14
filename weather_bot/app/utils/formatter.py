"""
Persian HTML formatting for weather messages.
"""

import html

from .translations import translate_condition


def _escape(text: str) -> str:
    """Escape HTML special characters to prevent injection."""
    return html.escape(text, quote=False)


def format_weather(data: dict) -> str:
    """
    Format single city weather data into Persian HTML.
    Expected WeatherAPI current.json structure.
    """
    location = data.get("location", {})
    current = data.get("current", {})
    condition = current.get("condition", {})

    city_name = _escape(str(location.get("name", "نامشخص")))
    country = _escape(str(location.get("country", "")))

    temp_c = current.get("temp_c", "—")
    feelslike_c = current.get("feelslike_c", "—")
    humidity = current.get("humidity", "—")
    wind_kph = current.get("wind_kph", "—")

    condition_code = condition.get("code")
    condition_text_en = condition.get("text", "")
    condition_fa = translate_condition(condition_text_en, condition_code)

    # Keep condition_fa as is (contains emoji), but ensure no HTML injection from original
    # translate_condition returns controlled Persian strings, safe.

    lines = [
        f"<b>🌤 وضعیت آب‌وهوای {city_name}</b>",
        f"🌍 <b>کشور:</b> {country}" if country else "",
        "━━━━━━━━━━━━━━",
        f"🌡 <b>دما:</b> {temp_c}°C",
        f"🥶 <b>احساس‌شده:</b> {feelslike_c}°C",
        f"💧 <b>رطوبت:</b> {humidity}٪",
        f"💨 <b>سرعت باد:</b> {wind_kph} km/h",
        f"☁️ <b>وضعیت:</b> {condition_fa}",
    ]
    # Filter empty lines
    return "\n".join([line for line in lines if line])


def format_compare(data1: dict, data2: dict) -> str:
    """
    Format comparison of two cities. Persian HTML.
    Calculates warmer city and temperature difference.
    """
    loc1 = data1.get("location", {})
    cur1 = data1.get("current", {})
    cond1 = cur1.get("condition", {})

    loc2 = data2.get("location", {})
    cur2 = data2.get("current", {})
    cond2 = cur2.get("condition", {})

    city1_name = _escape(str(loc1.get("name", "شهر اول")))
    city2_name = _escape(str(loc2.get("name", "شهر دوم")))

    temp1 = cur1.get("temp_c", 0)
    temp2 = cur2.get("temp_c", 0)

    # Ensure numeric
    try:
        temp1_f = float(temp1)
        temp2_f = float(temp2)
    except (ValueError, TypeError):
        temp1_f = 0
        temp2_f = 0

    feels1 = cur1.get("feelslike_c", "—")
    feels2 = cur2.get("feelslike_c", "—")
    hum1 = cur1.get("humidity", "—")
    hum2 = cur2.get("humidity", "—")
    wind1 = cur1.get("wind_kph", "—")
    wind2 = cur2.get("wind_kph", "—")

    cond1_fa = translate_condition(cond1.get("text", ""), cond1.get("code"))
    cond2_fa = translate_condition(cond2.get("text", ""), cond2.get("code"))

    diff = round(abs(temp1_f - temp2_f), 1)

    if temp1_f > temp2_f:
        warmer_line = f"🔥 <b>شهر گرم‌تر:</b> {city1_name}"
    elif temp2_f > temp1_f:
        warmer_line = f"🔥 <b>شهر گرم‌تر:</b> {city2_name}"
    else:
        warmer_line = "🌡 <b>دمای هر دو شهر برابر است.</b>"

    # Remove trailing .0 for integer diffs for cleaner display
    if diff == int(diff):
        diff_str = str(int(diff))
    else:
        diff_str = str(diff)

    template = (
        f"<b>⚖️ مقایسه آب‌وهوا</b>\n"
        f"\n"
        f"🏙 <b>{city1_name}</b>\n"
        f"🌡 {temp1}°C\n"
        f"🥶 احساس‌شده: {feels1}°C\n"
        f"💧 رطوبت: {hum1}٪\n"
        f"💨 باد: {wind1} km/h\n"
        f"{cond1_fa}\n"
        f"\n"
        f"━━━━━━━━━━━━\n"
        f"\n"
        f"🏙 <b>{city2_name}</b>\n"
        f"🌡 {temp2}°C\n"
        f"🥶 احساس‌شده: {feels2}°C\n"
        f"💧 رطوبت: {hum2}٪\n"
        f"💨 باد: {wind2} km/h\n"
        f"{cond2_fa}\n"
        f"\n"
        f"━━━━━━━━━━━━\n"
        f"\n"
        f"{warmer_line}\n"
    )

    # Only show diff if not equal
    if temp1_f != temp2_f:
        template += f"📊 <b>اختلاف دما:</b> {diff_str}°C"
    else:
        # Already shown equality line, no need for diff
        pass

    return template
