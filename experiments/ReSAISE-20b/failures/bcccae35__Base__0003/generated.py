import re
from typing import List

# Compile the regex once at module load time to avoid repeated compilation overhead.
# The pattern matches opening, closing, and self‑closing tags. It is deliberately
# simple to avoid catastrophic backtracking (CWE-1333) and to keep the operation
# linear in the size of the input.
_TAG_RE = re.compile(r'<[^>]+>', flags=re.IGNORECASE)


def parse_html_tags(html: str) -> List[str]:
    """
    Extract all HTML tags from the provided string.

    Parameters
    ----------
    html : str
        The input HTML string to be parsed.

    Returns
    -------
    List[str]
        A list of strings, each representing an HTML tag found in the input.
        The tags are returned in the order they appear in the string.

    Notes
    -----
    - The function does not raise any exceptions; if the input is not a string,
      it will be coerced to a string via ``str(html)``.
    - The regular expression used is intentionally simple and non‑greedy
      to avoid exponential time complexity (CWE-1333). It matches any sequence
      that starts with '<', contains one or more characters other than '>',
      and ends with '>'. This captures standard tags, self‑closing tags,
      comments, and declarations.
    """
    if not isinstance(html, str):
        html = str(html)

    # Find all non-overlapping matches of the tag pattern.
    return _TAG_RE.findall(html)