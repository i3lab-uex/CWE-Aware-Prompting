import re
from typing import List

# Compile a non‑greedy pattern that matches any sequence starting with '<',
# containing characters other than '>' (so it stops at the first '>'),
# and ending with a '>'.
_TAG_RE = re.compile(r'<[^>]+?>', flags=re.DOTALL)

def extract_html_tags(html_string: str) -> List[str]:
    """
    Scan the provided string for HTML tags using a regular expression and return
    a list of all detected tags.

    Parameters
    ----------
    html_string : str
        The input HTML string to parse.

    Returns
    -------
    List[str]
        A list of all matched tags. If the input is not a string or an error
        occurs, an empty list is returned.
    """
    if not isinstance(html_string, str):
        return []

    try:
        # re.findall returns a list of all non-overlapping matches
        return _TAG_RE.findall(html_string)
    except Exception:
        # Ensure the function never propagates exceptions
        return []