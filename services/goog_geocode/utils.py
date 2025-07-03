import unicodedata

import models


def address_components_city_country(addr_components: list[dict]) -> tuple[str, str]:
    """
    Get city name from list of google place address components.
    """
    locality_name = ""
    area_name = ""
    country_code = ""

    for addr_component in addr_components:
        # first check 'locality', then check 'administrative_area_level_1'

        if "locality" in addr_component.get("types", []):
            locality_name = (addr_component.get("long_name", "") or addr_component.get("longText", "")).lower()

        if "administrative_area_level_1" in addr_component.get("types", []):
            area_name = (addr_component.get("long_name", "") or addr_component.get("longText", "")).lower()

        if "country" in addr_component.get("types", []):
            country_code = (addr_component.get("short_name", "") or addr_component.get("shortText", "")).lower()

    if country_code in models.region.ASIA_CODES:
        # use area_name as city
        return country_code, name_remove_accents(name=area_name)
    else:
        # use locality_name as city
        return country_code, name_remove_accents(name=locality_name)


def name_remove_accents(name=str) -> str:
    """
    Removes accent marks (diacritics) from a Unicode string.
    """
    # Normalize the string to NFD (Normalization Form Canonical Decomposition)
    # This separates base characters from their combining diacritical marks.
    nfkd_form = unicodedata.normalize('NFKD', name)

    # Filter out characters that are combining diacritical marks ('Mn' category)
    # and join the remaining characters to form the new string.
    return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])
