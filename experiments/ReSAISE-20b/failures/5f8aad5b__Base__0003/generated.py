import re
from typing import List

def extract_html_tags(html_content: str) -> List[str]:
    """
    Extract all HTML tags from the given string.

    The function uses a non‑greedy regular expression that matches
    anything between '<' and the next '>' character.  It is designed
    to avoid catastrophic backtracking by limiting the amount of
    characters that can be matched inside a tag.

    Parameters:
        html_content (str): The HTML source string.

    Returns:
        List[str]: A list of matched tag strings, e.g.
                   ['<div>', '<img src="...">', ...].
    """
    if not isinstance(html_content, str):
        # If the input is not a string we simply return an empty list
        return []

    # Pattern: '<' followed by any number of characters that are not '>'
    # (non-greedy), then a closing '>'.
    tag_pattern = re.compile(r'<[^>]+?>', flags=re.IGNORECASE | re.DOTALL)

    # Find all matches; empty list if none
    return tag_pattern.findall(html_content)