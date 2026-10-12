import re
from typing import List

def detect_html_tags(html_str: str) -> List[str]:
    """
    Detects all HTML tags in the provided string using a regular expression.

    Parameters
    ----------
    html_str : str
        The input HTML content to be analyzed.

    Returns
    -------
    List[str]
        A list of strings, each representing a matched HTML tag.
    """
    if not isinstance(html_str, str):
        # Gracefully handle non-string input by returning an empty list.
        return []

    # Regular expression to match HTML tags, including attributes and self-closing tags.
    tag_pattern = re.compile(r'<[^>]+?>', flags=re.IGNORECASE)

    # Find all non-overlapping matches of the pattern.
    tags = tag_pattern.findall(html_str)

    return tags