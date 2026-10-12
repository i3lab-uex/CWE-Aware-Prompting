import re
from typing import List

def find_html_tags(html_string: str) -> List[str]:
    """
    Extracts all HTML tags from the provided string using a regular expression.

    Parameters
    ----------
    html_string : str
        The input HTML string from which tags should be extracted.

    Returns
    -------
    List[str]
        A list containing all matched HTML tags, including opening,
        closing, self‑closing tags and any attributes they may contain.
    """
    if not isinstance(html_string, str):
        # Gracefully handle non-string input by returning an empty list.
        return []

    # Regular expression to match anything that starts with '<' and ends with '>'
    # but does not include the closing '>' in a later tag.
    pattern = r'<[^>]+>'
    try:
        tags = re.findall(pattern, html_string)
        return tags
    except Exception:
        # In case of any unexpected regex errors, return an empty list.
        return []