import re
from typing import List

def grab_html_tags(html_code: str) -> List[str]:
    """
    Scan the provided HTML string for tags using a regular expression
    and return a list of all detected tag strings.

    Parameters
    ----------
    html_code : str
        The HTML content to parse.

    Returns
    -------
    List[str]
        A list containing every tag found in the input string.
        If an error occurs, an empty list is returned.

    Notes
    -----
    The regex pattern used here is deliberately simple and
    non-greedy (<[^>]+>) to avoid catastrophic backtracking
    (CWE-1333). It matches any sequence that starts with '<',
    followed by one or more characters that are not '>',
    and ends with a '>'.

    Examples
    --------
    >>> grab_html_tags('<div><p>Hello</p></div>')
    ['<div>', '<p>', '</p>', '</div>']
    """
    # Use a compiled, non-greedy regex pattern
    tag_pattern = re.compile(r'<[^>]+>')
    try:
        return tag_pattern.findall(html_code)
    except Exception:
        # Ensure no exception propagates
        return []