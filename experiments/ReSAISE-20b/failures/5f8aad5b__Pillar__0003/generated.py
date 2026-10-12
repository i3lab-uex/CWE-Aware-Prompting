import re
from typing import List

def extract_html_tags(html_content: str) -> List[str]:
    """
    Extracts HTML tags from the provided string using a regular expression.

    Parameters
    ----------
    html_content : str
        An HTML-formatted string to search for tags.

    Returns
    -------
    List[str]
        A list of tag strings found in the input. The tags include
        opening, closing, and self‑closing forms (e.g., "<div>", "</p>",
        "<img src='...'>").

    Notes
    -----
    * The function never raises an exception; any error results in an empty list.
    * It uses a non‑greedy, case‑insensitive pattern that matches common HTML tags.
    * The regex is intentionally conservative to avoid overmatching or
      processing malicious input that could trigger denial‑of‑service via
      catastrophic backtracking.
    """
    if not isinstance(html_content, str):
        return []

    # Regex pattern:
    #   <            - opening '<'
    #   \s*\/?       - optional whitespace and an optional '/' for closing tags
    #   \s*[a-zA-Z0-9]+  - tag name (letters or digits)
    #   [^>]*?       - any characters except '>' (non-greedy)
    #   >            - closing '>'
    pattern = r'<\s*\/?\s*[a-zA-Z0-9]+[^>]*?>'

    try:
        # re.IGNORECASE ensures tags like <DIV> are matched
        tags = re.findall(pattern, html_content, flags=re.IGNORECASE)
        return tags
    except Exception:
        # In the unlikely event of a regex error or other issue, return empty list
        return []