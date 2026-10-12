import re

def detect_html_tags(html_str: str) -> list[str]:
    """
    Detect all HTML tags in the given string using a regular expression.

    Parameters
    ----------
    html_str : str
        Input string containing HTML content.

    Returns
    -------
    list[str]
        A list of all substrings that match the pattern for an HTML tag.
        If no tags are found, returns an empty list.

    Notes
    -----
    The function uses a simple non-greedy regex pattern `<[^>]+>` which
    captures any sequence that starts with '<', contains characters other
    than '>' and ends with a '>'. This is efficient for typical use cases
    and avoids catastrophic backtracking because the character class
    `[^>]` never consumes a '>' which would otherwise lead to exponential
    matching time.
    """
    if not isinstance(html_str, str):
        # Gracefully handle non-string input by returning an empty list
        return []

    try:
        pattern = re.compile(r'<[^>]+>')
        # Using findall to get all non-overlapping matches
        return pattern.findall(html_str)
    except Exception:
        # In the unlikely event of a regex compilation or matching error,
        # return an empty list to avoid raising exceptions.
        return []