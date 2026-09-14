"""
Persian to English city name mapping.
Supports Persian city names and falls back to original input for WeatherAPI.
"""

# Comprehensive Persian -> English mapping
PERSIAN_CITY_MAP: dict[str, str] = {
    "تهران": "Tehran",
    "مشهد": "Mashhad",
    "اصفهان": "Isfahan",
    "شیراز": "Shiraz",
    "تبریز": "Tabriz",
    "کرج": "Karaj",
    "قم": "Qom",
    "اهواز": "Ahvaz",
    "رشت": "Rasht",
    "یزد": "Yazd",
    "کرمان": "Kerman",
    "ارومیه": "Urmia",
    "ارومیه": "Urmia",
    "زاهدان": "Zahedan",
    "همدان": "Hamadan",
    "کرمانشاه": "Kermanshah",
    "اردبیل": "Ardabil",
    "بندرعباس": "Bandar Abbas",
    "اراک": "Arak",
    "اسلامشهر": "Eslamshahr",
    "زنجان": "Zanjan",
    "سنندج": "Sanandaj",
    "قزوین": "Qazvin",
    "خرم‌آباد": "Khorramabad",
    "خرم آباد": "Khorramabad",
    "گرگان": "Gorgan",
    "ساری": "Sari",
    "بابل": "Babol",
    "آمل": "Amol",
    "نیشابور": "Neyshabur",
    "کاشان": "Kashan",
    "بوشهر": "Bushehr",
    "سمنان": "Semnan",
    "یاسوج": "Yasuj",
    "بجنورد": "Bojnord",
    "بیرجند": "Birjand",
    "ایللام": "Ilam",
    "ایلام": "Ilam",
    "شهرکرد": "Shahrekord",
    "دزفول": "Dezful",
    "آبادان": "Abadan",
    "خرمشهر": "Khorramshahr",
    "مراغه": "Maragheh",
    "ساوه": "Saveh",
    "نجف آباد": "Najafabad",
    "نجف‌آباد": "Najafabad",
    "قائمشهر": "Qaem Shahr",
    "قرچک": "Qarchak",
    "ورامین": "Varamin",
    "ملارد": "Malard",
    "سیرجان": "Sirjan",
    "بندرانزلی": "Bandar Anzali",
    "بندر انزلی": "Bandar Anzali",
}


def normalize_city(city: str) -> str:
    """
    Convert Persian city name to English for WeatherAPI.
    If city is not in mapping, return the original input stripped.
    Supports both Persian and English inputs.
    """
    if not city:
        return city

    cleaned = city.strip()

    # Direct mapping lookup (exact match)
    if cleaned in PERSIAN_CITY_MAP:
        return PERSIAN_CITY_MAP[cleaned]

    # Try normalized version without zero-width characters and extra spaces
    normalized = cleaned.replace("\u200c", "").replace("‌", "").strip()
    if normalized in PERSIAN_CITY_MAP:
        return PERSIAN_CITY_MAP[normalized]

    # Fallback: send original to WeatherAPI (it supports many languages/cities)
    return cleaned


def is_persian(text: str) -> bool:
    """Check if text contains Persian characters."""
    for ch in text:
        if "\u0600" <= ch <= "\u06FF":
            return True
    return False
