import re
from typing import List

# Regular expression pattern to match HTML tags.
# It captures opening, closing, and self‑closing tags without any attributes processing.
_TAG_RE = re.compile(r'<\s*\/?\s*[a-zA-Z0-9]+[^>]*?>', re.UNICODE)

def get_html_tags(html_input: str) -> List[str]:
    """
    Extract all HTML tags from the given string.

    Parameters
    ----------
    html_input : str
        A string containing HTML markup.

    Returns
    -------
    List[str]
        A list of tags found in the input string, preserving their order.
        If no tags are found an empty list is returned.

    Notes
    -----
    The function is intentionally simple and does not attempt to parse nested
    structures or validate the HTML. It uses a non‑capturing regex that is safe
    for typical usage and avoids common pitfalls such as greedy matching.
    """
    if not isinstance(html_input, str):
        # Defensive: return empty list for non‑string input instead of raising.
        return []

    try:
        # Find all matches; each match is a complete tag string.
        tags = _TAG_RE.findall(html_input)
        return tags
    except re.error:
        # In the unlikely event of a regex error, fall back to an empty list.
        return []