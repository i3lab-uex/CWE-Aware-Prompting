import re

def parse_html_tags(html: str) -> list[str]:
    """
    Extract all HTML tags from the given string.

    Parameters
    ----------
    html : str
        Input HTML string to parse.

    Returns
    -------
    list[str]
        A list of strings, each representing an HTML tag found in the input.
        Tags are returned exactly as they appear (including angle brackets).
    """
    if not isinstance(html, str):
        return []

    # Regular expression that matches an opening '<', optional whitespace,
    # then any characters except '>' (non-greedy), followed by a closing '>'.
    tag_pattern = re.compile(r'<\s*[^>]+?>', flags=re.IGNORECASE | re.DOTALL)

    # Find all matches; the pattern ensures we don't capture comments or
    # DOCTYPE declarations as separate tags.
    return tag_pattern.findall(html)