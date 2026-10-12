import re
from typing import List

# Compile a simple, efficient regex that matches any HTML tag.
# It avoids nested quantifiers and backtracking by using a non-greedy match
# for the tag content up to the next '>' character.
_TAG_RE = re.compile(r'<[^>]+>', re.IGNORECASE | re.DOTALL)

def find_html_tags(html_content: str) -> List[str]:
    """
    Return a list of all substrings in `html_content` that match the pattern
    for an HTML tag. The function is tolerant to malformed input and does
    not raise exceptions.

    Parameters:
        html_content (str): The HTML content to parse.

    Returns:
        List[str]: A list of matched tag strings, in the order they appear.
    """
    if not isinstance(html_content, str):
        # Gracefully handle non-string input by converting to string.
        try:
            html_content = str(html_content)
        except Exception:
            # If conversion fails, return an empty list.
            return []

    # Find all non-overlapping matches of the tag pattern.
    return _TAG_RE.findall(html_content)