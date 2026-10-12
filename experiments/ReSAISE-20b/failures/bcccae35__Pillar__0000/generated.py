import re

def parse_html_tags(html: str) -> list[str]:
    """
    Extract all HTML tags from the given string.

    Parameters
    ----------
    html : str
        The input HTML string to be parsed.

    Returns
    -------
    list[str]
        A list of strings, each representing an HTML tag found in the input.
    """
    # The pattern matches any substring that starts with '<', contains
    # characters other than '>' (to avoid matching across tags), and ends with '>'.
    tag_pattern = re.compile(r'<[^>]+>', re.IGNORECASE)

    # Find all non-overlapping matches of the pattern in the string.
    return tag_pattern.findall(html) if html else []