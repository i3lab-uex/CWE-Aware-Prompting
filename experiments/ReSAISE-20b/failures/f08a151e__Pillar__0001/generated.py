import re
from typing import List

def get_html_tags(html_input: str) -> List[str]:
    """
    Extracts all HTML tag names from the given string.

    The function uses a regular expression that matches opening and closing tags
    (including self‑closing ones). It returns a list of tag names in the order they
    appear. The function never raises an exception; any error during parsing
    results in an empty list being returned.

    Parameters
    ----------
    html_input : str
        A string containing HTML content.

    Returns
    -------
    List[str]
        A list of tag names found in the input string.
    """
    if not isinstance(html_input, str):
        # If input is not a string we cannot parse; return empty list.
        return []

    try:
        # The pattern captures the tag name following '<' or '</', ignoring
        # any leading whitespace. It does not capture the attributes.
        tag_pattern = re.compile(r'<\s*/?\s*([a-zA-Z0-9]+)', re.IGNORECASE)
        return tag_pattern.findall(html_input)
    except Exception:
        # In case of any unexpected error, return an empty list
        return []