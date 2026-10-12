import re

def find_html_tags(html_string: str):
    """
    Extract all HTML tags from the given string.

    Parameters
    ----------
    html_string : str
        The input HTML content.

    Returns
    -------
    list[str]
        A list of tag strings, e.g. ['<div>', '<img src="x">', '</p>'].
    """
    if not isinstance(html_string, str):
        # Gracefully handle non-string input
        return []

    # Regular expression to capture anything that starts with '<' and ends with '>'
    # It also ensures we don't accidentally match strings across newlines by using DOTALL
    tag_pattern = re.compile(r'<[^>]+>', flags=re.DOTALL)

    # Find all non-overlapping matches
    tags = tag_pattern.findall(html_string)

    return tags