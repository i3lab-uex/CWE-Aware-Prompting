import re
from typing import List

# Compile a safe, non‑backtracking regex pattern for HTML tags.
_TAG_PATTERN = re.compile(r"<[^>]+?>", re.IGNORECASE)

def extract_html_tags(html_content: str) -> List[str]:
    """
    Extracts all HTML tags from the provided string.

    Parameters
    ----------
    html_content : str
        A string containing HTML markup.

    Returns
    -------
    List[str]
        A list of tag strings (including the angle brackets). The order
        matches their appearance in the input string.

    Notes
    -----
    * The function never raises exceptions for normal inputs.
      In case of an unexpected type, a ``ValueError`` is raised with
      a clear message.
    * The regex pattern is deliberately simple and non‑backtracking
      to avoid catastrophic backtracking (CWE‑407).  It matches the
      smallest possible sequence between a '<' and the next '>'.

    Examples
    --------
    >>> extract_html_tags('<div><p>Text</p></div>')
    ['<div>', '<p>', '</p>', '</div>']
    """
    if not isinstance(html_content, str):
        raise ValueError("html_content must be a string")

    # Find all matches; re.findall returns the matched substrings.
    return _TAG_PATTERN.findall(html_content)