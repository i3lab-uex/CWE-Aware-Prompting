import re
from typing import List

# Pre‑compile a safe, non‑backtracking regex that captures the tag name
_TAG_RE = re.compile(r'<\s*/?\s*([a-zA-Z0-9]+)', flags=re.IGNORECASE)

def find_html_tags(html_string: str) -> List[str]:
    """
    Extract all HTML tag names from the given string.

    Parameters
    ----------
    html_string : str
        A string containing HTML markup.

    Returns
    -------
    List[str]
        A list of tag names (without angle brackets or attributes) in the order
        they appear. The function never raises an exception for normal input.
    """
    if not isinstance(html_string, str):
        # Gracefully handle non‑string input by returning an empty list
        return []

    try:
        # findall returns the captured group (tag name) for each match
        return _TAG_RE.findall(html_string)
    except Exception:
        # In the unlikely event of a regex error, return an empty list
        return []