import re
from typing import List

# Compile the regex once to avoid repeated compilation overhead.
# The pattern matches any opening '<', followed by one or more
# characters that are not '>' (non-greedy), and then a closing '>'.
# This simple pattern avoids catastrophic backtracking.
_TAG_RE = re.compile(r'<[^>]+>')

def grab_html_tags(html_code: str) -> List[str]:
    """
    Return a list of all HTML tags found in *html_code*.

    Parameters
    ----------
    html_code : str
        The input string containing HTML markup.

    Returns
    -------
    List[str]
        A list of matched tag strings, e.g. ['<div>', '</p>'].
    """
    if not isinstance(html_code, str):
        # If the input is not a string we simply return an empty list.
        return []

    try:
        # Find all non-overlapping matches of the tag pattern.
        tags = _TAG_RE.findall(html_code)
    except re.error:
        # In the unlikely event that regex compilation fails, return empty list.
        tags = []

    return tags