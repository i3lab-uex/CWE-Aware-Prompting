import re
from typing import List

# Compile the regex once to improve performance.
# The pattern matches any substring that starts with '<', ends with '>',
# and contains any characters except '>' in between (non-greedy).
_TAG_RE = re.compile(r"<[^>]+?>")

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
        A list of all tag substrings found in `html_string`. The tags
        include the surrounding angle brackets and any attributes.
    """
    # Guard against None input; treat as empty string.
    if not isinstance(html_string, str):
        return []

    # Use findall to avoid creating many intermediate objects.
    try:
        tags = _TAG_RE.findall(html_string)
    except re.error:
        # In the unlikely event of a regex error, return empty list.
        tags = []

    return tags