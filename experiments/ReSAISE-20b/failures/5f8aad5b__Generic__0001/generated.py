import re

def extract_html_tags(html_content: str) -> list:
    """
    Extract all HTML tag names from a given string.

    Parameters
    ----------
    html_content : str
        A string containing HTML content.

    Returns
    -------
    list[str]
        A list of tag names (without attributes or slashes) found in the input.
        The order corresponds to the order of appearance in the string.

    Notes
    -----
    - Self-closing tags, closing tags and opening tags are all captured.
    - The function is tolerant to malformed HTML; it simply ignores anything that
      does not match the tag pattern.
    """
    if not isinstance(html_content, str):
        # If something else is passed, return empty list to avoid errors
        return []

    # Regular expression that matches opening/closing/self-closing tags and captures the tag name
    tag_pattern = re.compile(r'<\s*/?\s*([a-zA-Z0-9]+)[^>]*?>', re.IGNORECASE)

    # Find all matches; group(1) contains the tag name
    return [match.group(1).lower() for match in tag_pattern.finditer(html_content)]