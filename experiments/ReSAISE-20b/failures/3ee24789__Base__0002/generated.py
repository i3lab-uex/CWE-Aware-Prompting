import re
from typing import List

# Pre-compiled regular expression to find simple HTML tags.
# This pattern matches any sequence that starts with '<', followed by one or more
# characters that are not '>', and ends with '>'. It is non-greedy and linear in
# time, mitigating CWE-1333 risks.
_TAG_REGEX = re.compile(r'<[^>]+>')

def detect_html_tags(html_str: str) -> List[str]:
    """
    Identify all HTML tags in the given string.

    Parameters
    ----------
    html_str : str
        The input HTML content to be analyzed.

    Returns
    -------
    List[str]
        A list of all substrings that match the pattern for an HTML tag.
        If no tags are found, returns an empty list.

    Notes
    -----
    The function does not raise any exceptions; invalid input simply yields an empty list.
    """
    if not isinstance(html_str, str):
        return []

    # Find all non-overlapping matches of the tag pattern.
    return _TAG_REGEX.findall(html_str)