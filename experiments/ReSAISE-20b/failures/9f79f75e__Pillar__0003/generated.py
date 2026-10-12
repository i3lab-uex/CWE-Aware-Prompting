import re
from typing import List

def find_html_tags(html_string: str) -> List[str]:
    """
    Extract all HTML tags from the given string.

    The function uses a non-greedy regular expression to match substrings that
    start with '<', contain any characters except '>' and end with a single
    '>'. It does not attempt to parse malformed HTML; it simply returns all
    tag-like substrings. No exceptions are raised for normal input.

    Parameters:
        html_string (str): The HTML content to scan.

    Returns:
        List[str]: A list of matched tag strings, e.g. ['<div>', '<img src="x">'].
    """
    # Compile the pattern once to avoid recompilation on each call
    _tag_pattern = re.compile(r'<[^>]+?>')

    # Find all non-overlapping matches
    tags = _tag_pattern.findall(html_string)

    return tags