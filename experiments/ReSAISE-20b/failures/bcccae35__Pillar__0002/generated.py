import re

def parse_html_tags(html: str) -> list[str]:
    """
    Extract all HTML tags from the input string.

    Parameters
    ----------
    html : str
        The input HTML content.

    Returns
    -------
    list[str]
        A list of all tags found in the input string. Each tag includes
        its surrounding angle brackets and any attributes.
    """
    if not isinstance(html, str):
        # Gracefully handle non‑string input by returning an empty list
        return []

    # Simple, efficient pattern that matches any sequence starting with '<',
    # followed by one or more characters that are not '>', and ending with '>'.
    tag_pattern = r'<[^>]+>'
    try:
        return re.findall(tag_pattern, html)
    except Exception:
        # In the unlikely event that regex fails (e.g., due to malformed input),
        # return an empty list rather than raising.
        return []