import re
from typing import List

# Compile the regular expression once to avoid repeated compilation overhead.
_TAG_RE = re.compile(
    r'<\s*/?\s*([a-zA-Z0-9]+)[^>]*>',  # capture the tag name
    re.IGNORECASE | re.UNICODE
)

def extract_html_tags(html_content: str) -> List[str]:
    """
    Extract all HTML tag names from the given string.

    Parameters
    ----------
    html_content : str
        A string containing HTML content.

    Returns
    -------
    List[str]
        A list of tag names found in the input string. The tags are returned
        in the order they appear and without surrounding angle brackets.
    """
    if not isinstance(html_content, str):
        # Gracefully handle non‑string input by returning an empty list.
        return []

    try:
        # Find all matches and extract the captured group (tag name).
        tags = [match.group(1) for match in _TAG_RE.finditer(html_content)]
    except Exception:
        # In case of any unforeseen error (e.g., regex engine failure),
        # return an empty list to avoid propagating exceptions.
        tags = []

    return tags