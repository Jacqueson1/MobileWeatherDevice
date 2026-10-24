# Each list is checked against the END of the phrase.
AREAS = [
    ("di kawasan pedalaman", "inland areas"),
    ("di kawasan pantai", "coastal areas"),
]

# (malay, english, rain_level 1-4)
EXTENTS = [
    ("di satu dua tempat", "isolated", 1),
    ("di beberapa tempat", "scattered", 2),
    ("di kebanyakan tempat", "most places", 3),
    ("menyeluruh", "widespread", 4),
]

# malay -> (kind, english, rain_level when no extent is given)
TYPES = {
    "tiada hujan": ("none", "no rain", 0),
    "jerebu": ("haze", "haze", 0),
    "mendung": ("overcast", "overcast", 0),
    "hujan": ("rain", "rain", 3),            # plain "hujan" has no extent: level is a guess
    "ribut petir": ("thunderstorm", "thunderstorms", 3),  # same guess
}


def translate(phrase):
    """Turn a Malay forecast phrase into English plus a rain level (0-4)."""
    text = (phrase or "").strip().lower()
    area = None
    extent = None
    level = None

    for malay, english in AREAS:
        if text.endswith(malay):
            area = english
            text = text[: -len(malay)].strip()
            break

    for malay, english, lvl in EXTENTS:
        if text.endswith(malay):
            extent = english
            level = lvl
            text = text[: -len(malay)].strip()
            break

    if text not in TYPES:
        # Unknown phrase: show it as-is so nothing is ever hidden
        return {"english": phrase, "kind": "unknown", "rain_level": None,
                "extent": None, "area": None, "known": False}

    kind, kind_en, default_level = TYPES[text]
    if level is None:
        level = default_level

    if extent is None or kind == "none":
        english = kind_en
    elif extent == "most places":
        english = f"{kind_en} in most places"
    else:
        english = f"{extent} {kind_en}"

    if area:
        english += f" ({area})"

    return {"english": english[0].upper() + english[1:], "kind": kind,
            "rain_level": level, "extent": extent, "area": area, "known": True}