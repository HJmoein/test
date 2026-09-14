"""
Dedicated translation function for WeatherAPI condition texts/codes to Persian with emojis.
"""

# Mapping by WeatherAPI condition code -> Persian with emoji
CONDITION_BY_CODE: dict[int, str] = {
    1000: "☀️ آفتابی",  # Sunny / Clear
    1003: "🌤 نیمه‌ابری",  # Partly cloudy
    1006: "☁️ ابری",  # Cloudy
    1009: "☁️ کاملاً ابری",  # Overcast
    1030: "🌫 مه‌آلود",  # Mist
    1063: "🌧 باران پراکنده",  # Patchy rain possible
    1066: "🌨 برف پراکنده",  # Patchy snow possible
    1069: "🌧❄️ باران و برف پراکنده",  # Patchy sleet possible
    1072: "🌧 نم‌نم باران یخ‌زده",  # Patchy freezing drizzle possible
    1087: "⛈ طوفان تندری",  # Thundery outbreaks possible
    1114: "❄️ کولاک",  # Blowing snow
    1117: "❄️ کولاک شدید",  # Blizzard
    1135: "🌫 مه‌آلود",  # Fog
    1147: "🌫 مه یخ‌زده",  # Freezing fog
    1150: "🌧 نم‌نم باران پراکنده",  # Patchy light drizzle
    1153: "🌧 نم‌نم باران",  # Light drizzle
    1168: "🌧 نم‌نم یخ‌زده",  # Freezing drizzle
    1171: "🌧 نم‌نم یخ‌زده شدید",  # Heavy freezing drizzle
    1180: "🌧 باران سبک پراکنده",  # Patchy light rain
    1183: "🌧 بارانی سبک",  # Light rain
    1186: "🌧 بارانی متوسط",  # Moderate rain at times
    1189: "🌧 بارانی متوسط",  # Moderate rain
    1192: "🌧 بارانی شدید",  # Heavy rain at times
    1195: "🌧 بارانی شدید",  # Heavy rain
    1198: "🧊 باران یخ‌زده سبک",  # Light freezing rain
    1201: "🧊 باران یخ‌زده شدید",  # Moderate or heavy freezing rain
    1204: "🌧❄️ برف و باران سبک",  # Light sleet
    1207: "🌧❄️ برف و باران شدید",  # Moderate or heavy sleet
    1210: "❄️ برف سبک پراکنده",  # Patchy light snow
    1213: "❄️ برفی سبک",  # Light snow
    1216: "❄️ برف پراکنده",  # Patchy moderate snow
    1219: "❄️ برفی متوسط",  # Moderate snow
    1222: "❄️ برف پراکنده شدید",  # Patchy heavy snow
    1225: "❄️ برفی سنگین",  # Heavy snow
    1237: "🧊 تگرگ",  # Ice pellets
    1240: "🌦 رگبار سبک",  # Light rain shower
    1243: "🌧 رگبار متوسط تا شدید",  # Moderate or heavy rain shower
    1246: "🌧 رگبار سیل‌آسا",  # Torrential rain shower
    1249: "🌧❄️ رگبار برف و باران",  # Light sleet showers
    1252: "🌧❄️ رگبار شدید برف و باران",  # Moderate or heavy sleet showers
    1255: "🌨 رگبار برف سبک",  # Light snow showers
    1258: "❄️ رگبار برف شدید",  # Moderate or heavy snow showers
    1261: "🧊 رگبار تگرگ سبک",  # Light showers of ice pellets
    1264: "🧊 رگبار تگرگ شدید",  # Moderate or heavy showers of ice pellets
    1273: "⛈ باران سبک با رعد و برق",  # Patchy light rain with thunder
    1276: "⛈ باران شدید با رعد و برق",  # Moderate or heavy rain with thunder
    1279: "⛈ برف سبک با رعد و برق",  # Patchy light snow with thunder
    1282: "⛈ برف سنگین با رعد و برق",  # Moderate or heavy snow with thunder
}

# Fallback mapping by lowercased English text
CONDITION_BY_TEXT: dict[str, str] = {
    "sunny": "☀️ آفتابی",
    "clear": "🌙 صاف",
    "partly cloudy": "🌤 نیمه‌ابری",
    "cloudy": "☁️ ابری",
    "overcast": "☁️ کاملاً ابری",
    "mist": "🌫 مه‌آلود",
    "fog": "🌫 مه‌آلود",
    "freezing fog": "🌫 مه یخ‌زده",
    "patchy rain possible": "🌧 باران پراکنده",
    "patchy snow possible": "🌨 برف پراکنده",
    "patchy sleet possible": "🌧❄️ باران و برف پراکنده",
    "patchy freezing drizzle possible": "🌧 نم‌نم یخ‌زده",
    "thundery outbreaks possible": "⛈ طوفان تندری",
    "blowing snow": "❄️ کولاک",
    "blizzard": "❄️ کولاک شدید",
    "light drizzle": "🌧 نم‌نم باران",
    "patchy light drizzle": "🌧 نم‌نم پراکنده",
    "freezing drizzle": "🌧 باران یخ‌زده",
    "heavy freezing drizzle": "🌧 باران یخ‌زده شدید",
    "patchy light rain": "🌧 باران پراکنده",
    "light rain": "🌧 بارانی سبک",
    "moderate rain at times": "🌧 بارانی متوسط",
    "moderate rain": "🌧 بارانی متوسط",
    "heavy rain at times": "🌧 بارانی شدید",
    "heavy rain": "🌧 بارانی شدید",
    "light freezing rain": "🧊 باران یخ‌زده سبک",
    "moderate or heavy freezing rain": "🧊 باران یخ‌زده شدید",
    "light sleet": "🌧❄️ برف و باران سبک",
    "moderate or heavy sleet": "🌧❄️ برف و باران شدید",
    "patchy light snow": "❄️ برف پراکنده",
    "light snow": "❄️ برفی سبک",
    "patchy moderate snow": "❄️ برف پراکنده",
    "moderate snow": "❄️ برفی متوسط",
    "patchy heavy snow": "❄️ برف شدید پراکنده",
    "heavy snow": "❄️ برفی سنگین",
    "ice pellets": "🧊 تگرگ",
    "light rain shower": "🌦 رگبار سبک",
    "moderate or heavy rain shower": "🌧 رگبار شدید",
    "torrential rain shower": "🌧 رگبار سیل‌آسا",
    "light sleet showers": "🌧❄️ رگبار برف و باران",
    "moderate or heavy sleet showers": "🌧❄️ رگبار شدید برف و باران",
    "light snow showers": "🌨 رگبار برف",
    "moderate or heavy snow showers": "❄️ رگبار برف شدید",
    "light showers of ice pellets": "🧊 رگبار تگرگ",
    "moderate or heavy showers of ice pellets": "🧊 رگبار تگرگ شدید",
    "patchy light rain with thunder": "⛈ باران با رعد و برق",
    "moderate or heavy rain with thunder": "⛈ باران شدید با رعد و برق",
    "patchy light snow with thunder": "⛈ برف با رعد و برق",
    "moderate or heavy snow with thunder": "⛈ برف سنگین با رعد و برق",
    "rain": "🌧 بارانی",
    "snow": "❄️ برفی",
    "thunderstorm": "⛈ طوفان تندری",
    "thunder": "⛈ رعد و برق",
    "drizzle": "🌧 نم‌نم باران",
    "sleet": "🌧❄️ برف و باران",
    "hail": "🧊 تگرگ",
}


def translate_condition(condition_text: str, condition_code: int | None = None) -> str:
    """
    Translate WeatherAPI condition to Persian with emoji.
    Priority: code -> exact text -> contains keyword fallback -> original.
    """
    # 1. Prefer code mapping (most reliable)
    if condition_code is not None and condition_code in CONDITION_BY_CODE:
        return CONDITION_BY_CODE[condition_code]

    if not condition_text:
        return "🌡 نامشخص"

    text_lower = condition_text.strip().lower()

    # 2. Exact text mapping
    if text_lower in CONDITION_BY_TEXT:
        return CONDITION_BY_TEXT[text_lower]

    # 3. Keyword fallback (for variations like "Light rain shower")
    for key, value in CONDITION_BY_TEXT.items():
        if key in text_lower or text_lower in key:
            # Only use if reasonably close
            if len(key) > 4:
                return value

    # 4. Fallback: return original with generic emoji
    return f"🌡 {condition_text}"
