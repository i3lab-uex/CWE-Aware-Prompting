import re
from typing import List

def detect_html_tags(html_str: str) -> List[str]:
    """
    Return a list of all HTML tags found in the input string.

    Parameters
    ----------
    html_str : str
        The HTML content to search for tags.

    Returns
    -------
    List[str]
        A list containing all matched tag strings.  If the input is empty
        or contains no tags, an empty list is returned.
    """
    if not html_str:
        return []

    # Simple regex that matches opening/closing tags, self‑closed tags,
    # and tags with attributes.  It deliberately does not attempt to
    # parse nested structures or validate tag names.
    pattern = r'<[^>]+>'
    return re.findall(pattern, html_str)