import re
from typing import List

def extract_html_tags(html_string: str) -> List[str]:
    """
    Extracts all HTML tags from the given string using a regular expression.

    Parameters
    ----------
    html_string : str
        The input HTML content to parse.

    Returns
    -------
    List[str]
        A list of all tags found in the input string. If no tags are found or an error occurs,
        an empty list is returned.
    """
    # Ensure the input is a string; if not, return an empty list
    if not isinstance(html_string, str):
        return []

    try:
        # Regex to match anything that starts with '<', ends with '>', and does not contain
        # a '>' inside (to avoid greediness). It also handles self-closing tags.
        pattern = r'<[^>]+>'
        return re.findall(pattern, html_string)
    except Exception:
        # In case of any unexpected error, return an empty list
        return []