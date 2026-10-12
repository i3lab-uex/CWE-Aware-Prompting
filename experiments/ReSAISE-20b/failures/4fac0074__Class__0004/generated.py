import re

# Pre‑compile a simple, non‑backtracking regex that matches HTML tags.
_TAG_RE = re.compile(r'<[^>]+>', flags=re.IGNORECASE)

def extract_html_tags(html_string: str):
    """
    Extract all HTML tags from the given string.

    Parameters
    ----------
    html_string : str
        Input text that may contain HTML markup.

    Returns
    -------
    list[str]
        A list of all substrings that match the pattern `<...>` in the order they appear.
    """
    if not isinstance(html_string, str):
        # Gracefully handle non‑string input without raising.
        return []

    try:
        # Find all matches; each match is a complete tag, including angle brackets.
        return _TAG_RE.findall(html_string)
    except Exception:
        # In the unlikely event that re throws, return an empty list.
        return []