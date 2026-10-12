import re
from typing import List

# Pre‑compile a simple, non‑greedy pattern to match HTML tags.
_TAG_PATTERN = re.compile(r'<[^>]+?>', flags=re.IGNORECASE)

def find_html_tags(html_content: str) -> List[str]:
    """
    Return a list of all substrings in *html_content* that look like HTML tags.

    The function uses a non‑greedy regular expression to avoid catastrophic
    backtracking on malformed or malicious input. It does not attempt to
    validate the tag structure beyond the simple presence of a leading '<'
    and a closing '>'.

    Parameters
    ----------
    html_content : str
        The string containing HTML markup to be scanned.

    Returns
    -------
    List[str]
        A list of matched tag strings.  If no tags are found, an empty list
        is returned.

    Notes
    -----
    * No exceptions are raised; malformed input simply results in fewer matches.
    * The pattern is intentionally conservative to mitigate the risk of
      CWE‑407 (inefficient algorithmic complexity) by avoiding greedy
      quantifiers that could lead to quadratic time on malicious input.
    """
    # Use findall for simplicity; the compiled regex ensures efficient matching.
    return _TAG_PATTERN.findall(html_content)