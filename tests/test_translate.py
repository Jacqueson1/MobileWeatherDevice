import pytest

from core.translate import translate

# All 17 phrases seen in the real data, lowercased
REAL_PHRASES = [
    "tiada hujan", "ribut petir", "ribut petir di beberapa tempat", "jerebu",
    "hujan di beberapa tempat", "hujan", "ribut petir di beberapa tempat di kawasan pedalaman",
    "ribut petir di kebanyakan tempat", "ribut petir menyeluruh", "hujan di kebanyakan tempat",
    "hujan di beberapa tempat di kawasan pedalaman", "mendung",
    "ribut petir di beberapa tempat di kawasan pantai",
    "hujan di beberapa tempat di kawasan pantai", "hujan menyeluruh",
    "ribut petir di kebanyakan tempat di kawasan pedalaman",
    "hujan di kebanyakan tempat di kawasan pedalaman",
]


@pytest.mark.parametrize("phrase", REAL_PHRASES)
def test_every_real_phrase_is_understood(phrase):
    assert translate(phrase)["known"] is True


def test_case_does_not_matter():
    assert translate("Tiada Hujan") == translate("tiada hujan")


def test_scattered_thunderstorms():
    result = translate("Ribut petir di beberapa tempat")
    assert result["english"] == "Scattered thunderstorms"
    assert result["rain_level"] == 2


def test_area_is_kept():
    result = translate("hujan di kebanyakan tempat di kawasan pedalaman")
    assert result["english"] == "Rain in most places (inland areas)"


def test_unknown_phrase_is_shown_as_is():
    result = translate("Salji")
    assert result["known"] is False
    assert result["english"] == "Salji"