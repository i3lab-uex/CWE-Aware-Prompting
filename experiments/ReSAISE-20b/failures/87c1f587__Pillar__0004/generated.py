import re
from typing import List

def find_html_tags(html_content: str) -> List[str]:
    """
    Return a list of all HTML tags found in the given string.

    Parameters
    ----------
    html_content : str
        The input HTML content to be analyzed.

    Returns
    -------
    List[str]
        A list of strings, each string being a matched HTML tag.
    """
    if not isinstance(html_content, str):
        # Gracefully handle non-string input without raising an exception
        return []

    # Regular expression to match HTML tags, including self-closing and attributes.
    tag_pattern = re.compile(r'<[^>]+?>', re.IGNORECASE)

    # Find all non-overlapping matches in the string
    tags = tag_pattern.findall(html_content)

    # Ensure that the result is always a list of strings
    return tags if tags else []