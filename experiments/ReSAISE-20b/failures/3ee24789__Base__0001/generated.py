import re

def detect_html_tags(html_str: str) -> list[str]:
    """
    Detect all HTML tags in the provided string using a safe, non‑capturing regular expression.
    
    The pattern `<[^>]+>` matches an opening '<', followed by one or more characters that are not
    '>', and a closing '>'. It is intentionally simple to avoid backtracking pitfalls such
    as those described in CWE‑1333. The function is tolerant to malformed input and never raises
    an exception – it simply returns an empty list if no tags are found or if the input is
    not a string.
    
    Parameters:
        html_str (str): The HTML content to analyze.

    Returns:
        list[str]: A list of matched tag strings. Empty if none are found.
    """
    if not isinstance(html_str, str):
        # Gracefully handle non‑string input
        return []

    try:
        pattern = re.compile(r'<[^>]+>')
        tags = pattern.findall(html_str)
    except Exception:
        # Any unexpected regex error results in an empty list
        tags = []

    return tags