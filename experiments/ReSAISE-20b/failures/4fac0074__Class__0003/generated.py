import re
from typing import List

def extract_html_tags(html_string: str) -> List[str]:
    """
    Extract all HTML tags from the provided string.

    Parameters
    ----------
    html_string : str
        The input HTML content to parse.

    Returns
    -------
    List[str]
        A list of all matched tags (including the surrounding angle brackets).
    """
    # Use a non-greedy pattern to avoid catastrophic backtracking.
    tag_pattern = re.compile(r'<[^>]+>', flags=re.DOTALL)

    try:
        # findall returns a list of all non-overlapping matches.
        return tag_pattern.findall(html_string)
    except Exception:
        # In case of any unexpected error, return an empty list instead of raising.
        return []