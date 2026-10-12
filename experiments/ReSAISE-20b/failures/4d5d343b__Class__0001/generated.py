import re
from typing import List

# Compile the regex once to avoid recompilation overhead.
_TAG_REGEX = re.compile(r'<[^>]*>', re.IGNORECASE | re.MULTILINE)

def grab_html_tags(html_code: str) -> List[str]:
    """
    Scan the provided string for HTML tags and return them as a list.

    Parameters
    ----------
    html_code : str
        The HTML string to parse.

    Returns
    -------
    List[str]
        A list containing all tags found in the input string.
        If no tags are found, an empty list is returned.

    Notes
    -----
    * The function is defensive: it will not raise an exception even if the input
      is not a string or contains unexpected content.
    * The regex used (`<[^>]*>`) is intentionally simple to avoid
      catastrophic backtracking and keep worst‑case complexity linear in the input size.
    """
    try:
        # Ensure we work with a string; if not, convert to str.
        text = str(html_code)
    except Exception:
        # In the unlikely event that conversion fails, return an empty list.
        return []

    try:
        # Find all non‑overlapping matches of the tag pattern.
        return _TAG_REGEX.findall(text)
    except Exception:
        # If something unexpected happens during regex matching, return an empty list.
        return []