import re
from typing import List

# Pre‑compile a non‑greedy regex that matches any HTML tag.
# The pattern is safe from catastrophic backtracking because it
# uses a simple character class and a non‑greedy quantifier.
_TAG_RE = re.compile(r'<[^>]+?>', flags=re.IGNORECASE | re.DOTALL)

def identify_html_tags(content: str) -> List[str]:
    """
    Scan the provided string for HTML tags using a regular expression
    and return a list of all detected tag strings.

    Parameters
    ----------
    content : str
        The input string containing potential HTML markup.

    Returns
    -------
    List[str]
        A list of matched tag strings.  If no tags are found an empty
        list is returned.

    Notes
    -----
    * The function never raises exceptions; any error results in an
      empty list.
    * The regex is intentionally simple and non‑greedy to avoid
      performance issues (CWE‑1333).
    """
    try:
        # Use findall to capture all matches as a list.
        return _TAG_RE.findall(content)
    except Exception:
        # In the unlikely event of an error, return an empty list.
        return []