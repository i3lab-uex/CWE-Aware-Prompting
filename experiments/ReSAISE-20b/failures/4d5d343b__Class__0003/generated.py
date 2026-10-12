import re
from typing import List

# Pre‑compile a non‑greedy pattern that matches any HTML tag.
# The pattern is intentionally simple and avoids nested quantifiers
# to prevent catastrophic backtracking (CWE‑407 mitigation).
_TAG_PATTERN = re.compile(r'<[^>]+>', flags=re.IGNORECASE | re.DOTALL)


def grab_html_tags(html_code: str) -> List[str]:
    """
    Scan the given HTML string and return a list of all tags found.

    The function is defensive:
      * It never raises an exception; malformed input simply results in
        an empty list or the tags that can be parsed.
      * It uses a pre‑compiled, non‑greedy regex to avoid excessive
        backtracking and keep worst‑case complexity linear in the input size.

    Parameters:
        html_code (str): The HTML source to scan.

    Returns:
        List[str]: A list of tag strings, e.g. ['<div>', '<a href="...">'].
    """
    if not isinstance(html_code, str):
        # If the caller passes a non‑string, return an empty list safely.
        return []

    try:
        # Find all matches of the tag pattern.
        tags = _TAG_PATTERN.findall(html_code)
    except Exception:
        # Any unforeseen error (e.g., regex engine failure) is swallowed
        # and results in an empty list to keep the function non‑exceptional.
        tags = []

    return tags