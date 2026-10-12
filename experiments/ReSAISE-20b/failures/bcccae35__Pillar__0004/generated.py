import re
from typing import List

def parse_html_tags(html: str) -> List[str]:
    """
    Extract all HTML tags from the input string.

    Args:
        html: The input HTML string to be parsed.

    Returns:
        A list of strings, each representing an HTML tag found in the input.
    """
    if not isinstance(html, str):
        return []

    # Regular expression to match tags.
    # < followed by any characters that are not '>' (non-greedy) and then a closing '>'.
    tag_pattern = re.compile(r'<[^>]+>', flags=re.IGNORECASE)

    # Find all matches; return empty list if none.
    tags = tag_pattern.findall(html)
    return tags