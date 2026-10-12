import re
from typing import List

def detect_html_tags(html_str: str) -> List[str]:
    """
    Detect all HTML tags in the provided string.

    Parameters
    ----------
    html_str : str
        The input HTML content to analyze.

    Returns
    -------
    List[str]
        A list of strings, each representing a matched HTML tag.
    """
    if not isinstance(html_str, str):
        # Guard against non-string input; return empty list instead of raising.
        return []

    # Regular expression to match HTML tags:
    #   < ... >  with optional leading slash and any attributes.
    tag_pattern = re.compile(r'<\s*/?\w[^>]*?>', flags=re.IGNORECASE)

    # Find all non-overlapping matches
    return tag_pattern.findall(html_str)