import re

def parse_html_tags(html: str) -> list[str]:
    """
    Extract all HTML tags from the given string.

    Parameters
    ----------
    html : str
        The input HTML content.

    Returns
    -------
    list[str]
        A list of strings, each string being an HTML tag found in the input.
    """
    if not isinstance(html, str):
        return []

    # Regex to match opening, closing, and self‑closing tags.
    # It captures everything between '<' and the next '>' without including
    # leading/trailing whitespace. The pattern does not attempt to validate
    # the tag names or attributes; it simply finds any sequence that starts
    # with '<' and ends with '>'.
    tag_pattern = r'<[^>]*?>'

    try:
        tags = re.findall(tag_pattern, html)
    except Exception:
        # In case of any unexpected error (e.g., malformed regex), return empty list
        tags = []

    return tags