import re
from typing import List

# Regular expression to match simple HTML tags.
# It looks for a '<', then any characters that are not '>' (non-greedy), and ends with '>'.
_TAG_RE = re.compile(r'<[^>]+?>')

def identify_html_tags(content: str) -> List[str]:
    """
    Scan the given HTML string for tags and return a list of all detected tags.

    Parameters
    ----------
    content : str
        The HTML string to parse.

    Returns
    -------
    List[str]
        A list of matched tag strings, e.g. ['<div>', '<img src="...">'].
        The list preserves the order of appearance in `content`.

    Notes
    -----
    - The function is intentionally conservative: it does not attempt to validate
      tag syntax or handle malformed input.  It simply captures any sequence that
      starts with '<' and ends with the next '>'.
    - The regex is deliberately simple to avoid catastrophic backtracking
      (CWE-407).  It uses a non-greedy match that stops at the first '>' after
      '<', ensuring linear complexity in the length of `content`.
    - Any exception raised during matching is caught and results in an empty
      list, guaranteeing that the function never propagates errors.
    """
    if not isinstance(content, str):
        return []

    try:
        # Find all non-overlapping matches of the pattern.
        return _TAG_RE.findall(content)
    except Exception:
        # In case of any unexpected error, return an empty list.
        return []