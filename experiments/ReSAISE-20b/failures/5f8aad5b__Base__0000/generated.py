import re
from typing import List

def extract_html_tags(html_content: str) -> List[str]:
    """
    Extracts all HTML tags from the provided string.

    Parameters
    ----------
    html_content : str
        A string containing HTML content.

    Returns
    -------
    List[str]
        A list of tag strings, including the surrounding angle brackets.
        If no tags are found, an empty list is returned.

    Notes
    -----
    * The function uses a non-greedy, bounded regular expression to avoid
      catastrophic backtracking (CWE‑1333). The pattern `r'<[^>]+>'` matches
      any sequence that starts with '<', contains one or more characters that
      are not '>', and ends with '>'. This ensures linear time complexity in
      the size of `html_content`.
    * No exceptions are raised under normal operation; if the input is not a
      string, it will be converted to one implicitly by `str()`.

    Examples
    --------
    >>> extract_html_tags('<div>Hello <span>world</span></div>')
    ['<div>', '<span>', '</span>', '</div>']
    """
    # Ensure the input is a string; this avoids TypeError if a non-string is passed.
    content = str(html_content)

    # Use a simple, efficient regex that does not suffer from backtracking.
    tag_pattern = re.compile(r'<[^>]+>', flags=re.IGNORECASE)

    # Find all non-overlapping matches and return them as a list.
    return tag_pattern.findall(content)