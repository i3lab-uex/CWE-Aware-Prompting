import re
from typing import List

# Pre‑compiled pattern that matches any HTML tag (opening, closing or self‑closing).
# The pattern is simple and avoids nested group constructs to prevent catastrophic
# backtracking (CWE‑664 related resource misuse).
_TAG_PATTERN = re.compile(r'<[^>]+?>', flags=re.IGNORECASE)

def extract_html_tags(html_content: str) -> List[str]:
    """
    Extract all HTML tags from the provided string.

    Parameters
    ----------
    html_content : str
        A string containing HTML markup.

    Returns
    -------
    List[str]
        A list of tag strings (e.g., ['<div>', '</p>', '<img src="..."/>']).
        The list preserves the order of appearance in the input.

    Notes
    -----
    * The function never raises exceptions during normal operation.
      If the input is not a string, it returns an empty list.
    * The regex is intentionally simple to avoid excessive resource consumption
      and potential denial‑of‑service scenarios.
    """
    if not isinstance(html_content, str):
        # Gracefully handle non‑string input without raising.
        return []

    try:
        # Find all tags; re.findall returns a list of matched substrings.
        return _TAG_PATTERN.findall(html_content)
    except Exception:
        # In case of an unexpected regex error, return empty list to avoid crashing.
        return []