import re
from typing import List

# Precompile a safe, non-greedy regex pattern that matches HTML tags.
# This pattern avoids catastrophic backtracking by using a negated
# character class and limiting the search to non-'>' characters.
_TAG_PATTERN = re.compile(r'<[^>]+>', flags=re.DOTALL)

def parse_html_tags(html: str) -> List[str]:
    """
    Extract all HTML tags from the input string.

    Args:
        html: The input HTML string to be parsed.

    Returns:
        A list of strings, each representing an HTML tag found in the input.
    """
    if not isinstance(html, str):
        # If the input is not a string, return an empty list without raising.
        return []

    # Find all non-overlapping matches of the tag pattern.
    tags = _TAG_PATTERN.findall(html)
    return tags