import re
from typing import List

# Compile a non-greedy regex pattern to match any HTML tag.
# The pattern avoids backtracking by using a lazy quantifier and
# disallowing nested '>' characters inside the tag.
_TAG_RE = re.compile(r'<[^>]+?>')

def parse_html_tags(html: str) -> List[str]:
    """
    Extract all HTML tags from the given string.

    Parameters
    ----------
    html : str
        The input HTML content.

    Returns
    -------
    List[str]
        A list of strings, each representing an HTML tag found in the input.
        The order corresponds to their appearance in the string.

    Notes
    -----
    - This function does not raise any exceptions; malformed input simply yields an empty list.
    - The regular expression is intentionally simple and non-greedy to avoid
      catastrophic backtracking (CWE-407).
    """
    if not isinstance(html, str):
        return []

    # Find all matches; the regex is compiled once for efficiency.
    tags = _TAG_RE.findall(html)
    return tags