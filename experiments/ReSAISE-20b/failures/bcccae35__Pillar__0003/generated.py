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
        If no tags are present or if `html` is empty, an empty list is returned.

    Notes
    -----
    - The function does not raise any exceptions; malformed input simply results in an empty list.
    - A simple regular expression is used to capture tags. It matches any
      substring that starts with '<', contains any characters except '>',
      and ends with '>'. This covers most common tag forms but does not
      validate HTML structure.
    """
    if not isinstance(html, str) or not html:
        return []

    # Pattern matches opening/closing tags and self‑closing tags.
    pattern = r'<[^>]+>'
    return re.findall(pattern, html)