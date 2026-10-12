import re
from typing import List

def find_html_tags(html_content: str) -> List[str]:
    """
    Return a list of all HTML tags found in the input string.

    A tag is any substring that starts with '<', ends with '>', and does not
    contain a '>' character in between. This simple definition covers
    opening tags, closing tags, self‑closing tags and comments.

    Parameters
    ----------
    html_content : str
        The input string containing potential HTML markup.

    Returns
    -------
    List[str]
        A list of matched tag strings in the order they appear.
    """
    if not isinstance(html_content, str):
        # If a non‑string is passed, simply return an empty list.
        return []

    # A straightforward pattern that avoids catastrophic backtracking:
    tag_pattern = re.compile(r'<[^>]+?>')
    return [match.group() for match in tag_pattern.finditer(html_content)]