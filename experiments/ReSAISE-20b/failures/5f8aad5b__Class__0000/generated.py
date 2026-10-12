import re
from typing import List

# Regular expression to match HTML tags.
#   - `<` starts a tag
#   - `[^>]*?` lazily matches any characters that are not `>`
#   - `>` ends the tag
_TAG_RE = re.compile(r'<[^>]*?>', re.DOTALL)

def extract_html_tags(html_content: str) -> List[str]:
    """
    Extract all HTML tags from the provided string.

    Parameters
    ----------
    html_content : str
        A string containing HTML content.

    Returns
    -------
    List[str]
        A list of tags found in `html_content`. The order is the same
        as they appear in the input string.

    Notes
    -----
    - The function is deliberately defensive: it catches any unexpected
      exceptions from the regex engine and returns an empty list instead.
    - The pattern is non‑greedy to avoid catastrophic backtracking
      (CWE-407) even when the input is maliciously crafted.
    """
    if not isinstance(html_content, str):
        return []

    try:
        # `findall` returns all non-overlapping matches of the pattern.
        return _TAG_RE.findall(html_content)
    except Exception:
        # In case of any unforeseen error, return an empty list.
        return []