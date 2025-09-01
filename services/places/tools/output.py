import models


def output_markdown(places: list[models.Place]) -> str:
    """
    Convert list of models to markdown text
    """

    md_list = []

    md_list.append(f"found {len(places)} places:\n\n")

    for i, place in enumerate(places):
        md_list.append(f"- {place.name}, {place.city}\n")

        if place.brands_count > 0:
            md_list.append(f"  brands: {place.brands_string}\n")

        if place.website:
            md_list.append(f"  website: {place.website}\n")

        md_list.append("\n")

    return "".join(md_list)
