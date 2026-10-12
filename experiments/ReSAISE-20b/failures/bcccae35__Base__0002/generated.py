import re

def parse_html_tags(html: str) -> list[str]:
    """
    Extract all HTML tags from the given string.

    Parameters
    ----------
    html : str
        The input HTML content to parse.

    Returns
    -------
    list[str]
        A list of all tags found in the input string, preserving order.
    """
    # The pattern matches any sequence that starts with '<', contains
    # one or more characters that are not '>', and ends with '>'.
    # It is non-greedy and linear in time, avoiding catastrophic backtracking.
    tag_pattern = re.compile(r'<[^>]+>')
    return [match.group() for match in tag_pattern.finditer(html)]