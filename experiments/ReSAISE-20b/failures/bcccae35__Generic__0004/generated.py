import re

def parse_html_tags(html: str) -> list[str]:
    """
    Extract all HTML tags from the given string.

    Parameters
    ----------
    html : str
        The input HTML string to be parsed.

    Returns
    -------
    list[str]
        A list of strings, each representing an HTML tag found in the input.
    """
    if not isinstance(html, str):
        # If non-string input is provided, return an empty list without raising.
        return []

    # Regular expression to match HTML tags:
    #   < followed by any characters except '>' (non-greedy), then >
    tag_pattern = re.compile(r'<[^>]+?>', flags=re.IGNORECASE)

    # Find all non-overlapping matches in the string
    return tag_pattern.findall(html)