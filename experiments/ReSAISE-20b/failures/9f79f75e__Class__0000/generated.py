import re
from typing import List

def find_html_tags(html_string: str) -> List[str]:
    """
    Extracts all HTML tags from the provided string.

    Parameters
    ----------
    html_string : str
        The input string containing HTML markup.

    Returns
    -------
    List[str]
        A list of all substrings that match the pattern of an HTML tag.
        The tags are returned in the order they appear in the input string.

    Notes
    -----
    * The function uses a non‑greedy regular expression to avoid catastrophic backtracking
      and keeps the algorithmic complexity linear with respect to the length of the input.
    * The pattern matches both opening and closing tags, as well as self‑closing tags,
      but it does not validate HTML syntax beyond the simple tag structure.
    * No exceptions are raised for malformed input; an empty list is returned if no tags
      are found.
    """
    # Non‑greedy match for any tag: < ... >
    pattern = re.compile(r'<[^>]*?>', re.DOTALL)
    return pattern.findall(html_string)