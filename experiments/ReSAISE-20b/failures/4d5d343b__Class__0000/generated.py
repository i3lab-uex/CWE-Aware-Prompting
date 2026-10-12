import re
from typing import List

# Compile the regular expression once. The pattern matches any sequence that starts with '<',
# followed by one or more characters that are not '>', and ends with '>'.  This is a simple
# non-greedy match that avoids catastrophic backtracking and does not attempt to parse nested tags.
TAG_RE = re.compile(r'<[^>]+?>', flags=re.IGNORECASE | re.DOTALL)


def grab_html_tags(html_code: str) -> List[str]:
    """
    Scan *html_code* for HTML tags and return a list of all detected tags.

    Parameters
    ----------
    html_code : str
        The input HTML string to be parsed.

    Returns
    -------
    List[str]
        A list containing each tag found in the input string, including angle brackets.
        The order of tags matches their appearance in *html_code*.

    Notes
    -----
    - The function is tolerant to malformed input and will not raise exceptions.
    - It uses a simple, efficient regular expression that is safe against
      catastrophic backtracking (CWE-407).
    """
    try:
        # Ensure the input is a string; if not, convert it to an empty string.
        if not isinstance(html_code, str):
            html_code = ''
    except Exception:
        # Any unexpected exception is caught; return an empty list.
        return []

    try:
        tags = TAG_RE.findall(html_code)
    except Exception:
        # In the unlikely event that regex matching fails, return an empty list.
        tags = []

    return tags