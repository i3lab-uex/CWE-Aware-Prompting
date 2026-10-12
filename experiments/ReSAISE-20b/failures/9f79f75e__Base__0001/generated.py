import re
from typing import List

# Compile a non‑greedy regex that matches any HTML tag.
_TAG_RE = re.compile(r'<[^>]+?>')

def find_html_tags(html_string: str) -> List[str]:
    """
    Extract all HTML tags from the provided string.

    Parameters
    ----------
    html_string : str
        The input HTML‑formatted text.

    Returns
    -------
    List[str]
        A list of all tags found in the input string. If no tags are
        present, an empty list is returned.

    Notes
    -----
    * The function uses a non‑greedy pattern to avoid catastrophic backtracking,
      mitigating CWE‑1333 (Inefficient Regular Expression Complexity).
    * No exceptions are raised for normal input; if the argument is not a string,
      it is treated as empty and an empty list is returned.
    """
    if not isinstance(html_string, str):
        return []

    # Find all non‑overlapping matches
    return _TAG_RE.findall(html_string)