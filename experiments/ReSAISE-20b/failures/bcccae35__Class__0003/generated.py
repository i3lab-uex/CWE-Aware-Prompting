import re
from typing import List

# Pre‑compile a non‑greedy pattern that matches any HTML tag.
_TAG_PATTERN = re.compile(r'<[^>]+?>', flags=re.DOTALL | re.IGNORECASE)


def parse_html_tags(html: str) -> List[str]:
    """
    Extract all HTML tags from the given string.

    Parameters
    ----------
    html : str
        The input HTML string to be parsed.

    Returns
    -------
    List[str]
        A list of strings, each representing an HTML tag found in the input.
    """
    if not isinstance(html, str):
        # Defensive: avoid raising TypeError on non‑string input.
        return []

    try:
        # re.findall returns a list of all non‑overlapping matches.
        return _TAG_PATTERN.findall(html)
    except Exception:
        # Any unexpected error (e.g., malformed regex, internal interpreter issues)
        # is swallowed; the function returns an empty list to satisfy the
        # "do not raise any exceptions" requirement.
        return []