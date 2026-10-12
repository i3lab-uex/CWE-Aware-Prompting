import re
from typing import List

# Compile a regex that matches any HTML tag (opening, closing or self‑closing).
_TAG_RE = re.compile(r'<[^>]*>', flags=re.IGNORECASE | re.DOTALL)

def extract_html_tags(html_string: str) -> List[str]:
    """
    Extract all HTML tags from the provided string.

    Parameters
    ----------
    html_string : str
        The input HTML content to search for tags.

    Returns
    -------
    List[str]
        A list of matched tag strings, e.g. ['<div>', '</span>'].
        Returns an empty list if no tags are found or input is not a string.

    Notes
    -----
    The function never raises an exception; it returns an empty list on any error.
    """
    try:
        if not isinstance(html_string, str):
            return []

        # Find all non-overlapping matches of the tag pattern.
        tags = _TAG_RE.findall(html_string)
        return tags
    except Exception:
        # Silently catch all exceptions and return an empty list.
        return []