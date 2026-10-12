import re

def extract_html_elements(document: str):
    """
    Extract all HTML tags from a string using a safe regular expression.

    Parameters
    ----------
    document : str
        The HTML content to analyze.

    Returns
    -------
    list[str]
        A list of all substrings that match HTML tags.
    """
    if not isinstance(document, str):
        return []

    # Use a non-greedy pattern that stops at the first '>' after '<'.
    # This avoids catastrophic backtracking (CWE-1333) and is efficient.
    pattern = re.compile(r'<[^>]+>', flags=re.IGNORECASE)

    try:
        tags = pattern.findall(document)
        return tags
    except Exception:
        # Any unexpected error results in an empty list rather than raising.
        return []