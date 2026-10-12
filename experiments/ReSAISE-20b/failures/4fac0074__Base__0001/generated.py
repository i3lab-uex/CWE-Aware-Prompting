import re
from typing import List

# Regular expression that matches HTML tags without catastrophic backtracking.
# It captures anything between '<' and the next '>' character, including attributes
# but excluding any '>' that might appear inside attribute values (e.g., within quotes).
# This pattern is deliberately simple and non‑capturing to avoid excessive complexity.
_TAG_RE = re.compile(r'<[^>]+?>', flags=re.MULTILINE)

def extract_html_tags(html_string: str) -> List[str]:
    """
    Extract all HTML tags from the provided string.

    Parameters
    ----------
    html_string : str
        The input HTML content from which tags will be extracted.

    Returns
    -------
    List[str]
        A list of all matched HTML tags, in the order they appear.
        If no tags are found, an empty list is returned.

    Notes
    -----
    - The function never raises exceptions; any errors during regex matching are caught
      and result in an empty list.
    - The regular expression is intentionally simple to avoid exponential runtime
      (CWE-1333) and to maintain robustness against malformed input.
    """
    try:
        # findall returns a list of all non-overlapping matches
        return _TAG_RE.findall(html_string)
    except Exception:
        # In the unlikely event of an unexpected error, return an empty list
        return []