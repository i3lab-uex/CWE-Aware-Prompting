import re
from typing import List

def find_html_tags(html_content: str) -> List[str]:
    """
    Find all HTML tags in the given string using a regular expression.

    Parameters
    ----------
    html_content : str
        The input HTML content to be analyzed.

    Returns
    -------
    List[str]
        A list of strings, each string being a matched HTML tag.
        The function never raises an exception; if the input is not a string,
        it will be coerced to ``str`` and an empty list will be returned.
    """
    # Ensure the input is a string; if not, convert it safely
    try:
        text = str(html_content)
    except Exception:
        return []

    # Regular expression to match tags (including self-closing, with attributes, etc.)
    tag_pattern = re.compile(r'<[^>]+>', flags=re.IGNORECASE)

    # Find all non-overlapping matches
    tags = tag_pattern.findall(text)

    return tags