import re
from typing import List

def extract_html_elements(document: str) -> List[str]:
    """
    Return a list of all HTML tags found in the input string.

    Parameters
    ----------
    document : str
        The HTML content to be analyzed.

    Returns
    -------
    List[str]
        All substrings that match an HTML tag pattern.
    """
    if not isinstance(document, str):
        # If the input is not a string we simply return an empty list.
        return []

    # A simple, non-greedy regex that matches any opening or closing tag,
    # including attributes and self-closing tags.
    pattern = r'<[^>]+>'
    try:
        return re.findall(pattern, document)
    except Exception:
        # In the unlikely event of a regex error we return an empty list.
        return []