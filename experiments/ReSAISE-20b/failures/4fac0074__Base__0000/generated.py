import re
from typing import List

def extract_html_tags(html_string: str) -> List[str]:
    """
    Extract all HTML tags from the provided string using a safe, non-greedy regular expression.
    
    Parameters
    ----------
    html_string : str
        The HTML content to search for tags.

    Returns
    -------
    List[str]
        A list containing every matched tag, including the surrounding angle brackets.
        If no tags are found an empty list is returned.

    Notes
    -----
    * The regex pattern `<[^>]+>` matches any substring that starts with '<',
      contains one or more characters that are not '>', and ends with '>'.
    * This pattern is non-greedy in the sense that it stops at the first '>'
      encountered, preventing catastrophic backtracking and keeping performance
      linear in the length of the input.
    * The function is defensive: it catches unexpected errors and returns an empty
      list rather than propagating exceptions.
    """
    # Ensure the input is a string; if not, return an empty list gracefully
    if not isinstance(html_string, str):
        return []

    # Compile the regex once for efficiency
    tag_pattern = re.compile(r"<[^>]+>")
    
    try:
        return tag_pattern.findall(html_string)
    except Exception:
        # Any unexpected error (e.g., malformed regex engine state) is swallowed
        return []