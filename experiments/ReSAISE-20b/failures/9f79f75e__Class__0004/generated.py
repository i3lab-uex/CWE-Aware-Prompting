import re
from typing import List

# Compile a simple, non‑backtracking regex that matches any HTML tag.
# The pattern looks for '<', then any characters that are not '>' (non‑greedy),
# and finally a closing '>'. This avoids catastrophic backtracking while still
# capturing standard tags, self‑closing tags, and comments.
_TAG_RE = re.compile(r'<[^>]+>')

def find_html_tags(html_string: str) -> List[str]:
    """
    Extract all HTML tags from a given string.

    Parameters
    ----------
    html_string : str
        The input string containing HTML markup.

    Returns
    -------
    List[str]
        A list of matched tag strings, in the order they appear.
        If no tags are found or the input is not a string, an empty list is returned.

    Notes
    -----
    - The function does **not** raise exceptions for normal inputs.
    - It uses a non‑backtracking regex to avoid CWE‑407 (inefficient algorithmic
      complexity) vulnerabilities.
    """
    if not isinstance(html_string, str):
        return []

    try:
        # findall returns all non‑overlapping matches of the pattern
        return _TAG_RE.findall(html_string)
    except Exception:
        # In case of any unforeseen error, return an empty list instead of raising
        return []