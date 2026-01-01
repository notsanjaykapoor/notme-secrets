import unicodedata

import models


def address_components_city_country(
    addr_components: list[dict],
) -> tuple[str, str, str, str]:
    """
    Get city name from list of google place address components.

    The address components list contains items like 'locality', 'country', 'administrative_area_1|2|3'.
    Most cities in north america use the locality field for the city.  Many of the asian countries
    seem to use administrative_area_as their 'city' components.

    Locality focuses on the city/town, while administrative area levels provide the hierarchical breakdown of the wider
    geographical region within which the locality exists.

    Note that the address components objects returned from the new google places api uses camel case (e.g. longText)
    while the google geocode api uses snake case (e.g. long_name).
    """
    locality_name = ""
    area_name = ""
    city_name = ""
    country_code = ""

    for addr_component in addr_components:
        # parse addr_component based on type

        if "administrative_area_level_1" in addr_component.get("types", []):
            area_name = addr_component.get("longText", "").lower() or addr_component.get("long_name", "").lower()
            area_name = name_remove_accents(name=area_name)

        if "country" in addr_component.get("types", []):
            country_code = addr_component.get("shortText", "").lower() or addr_component.get("short_name", "").lower()

        if "locality" in addr_component.get("types", []):
            locality_name = addr_component.get("longText", "").lower() or addr_component.get("long_name", "").lower()
            locality_name = name_remove_accents(name=locality_name)

        if "postal_town" in addr_component.get("types", []):
            town_name = addr_component.get("longText", "").lower() or addr_component.get("long_name", "").lower()
            town_name = name_remove_accents(name=town_name)

    if country_code in models.region.ASIA_CODES:
        city_name = area_name
        city_key = "administrative_area_level_1"
    elif country_code in models.region.GB_CODES:
        city_name = town_name
        city_key = "postal_town"
    else:
        city_name = locality_name
        city_key = "locality"

    if not city_name:
        # whoops, this probably means we need to look at a higher level administrative area for the "city" name
        raise ValueError(
            f"city name not found in '{city_key}' address component - area '{area_name}', locality '{locality_name}'"
        )

    return country_code, city_name, locality_name, area_name


def name_remove_accents(name=str) -> str:
    """
    Removes accent marks (diacritics) from a Unicode string.
    """
    # Normalize the string to NFD (Normalization Form Canonical Decomposition)
    # This separates base characters from their combining diacritical marks.
    nfkd_form = unicodedata.normalize("NFKD", str(name))

    # Filter out characters that are combining diacritical marks ('Mn' category)
    # and join the remaining characters to form the new string.
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])
