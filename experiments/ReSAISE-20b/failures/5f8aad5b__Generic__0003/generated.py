import re
from typing import List

def extract_html_tags(html_content: str) -> List[str]:
    """
    Extract all HTML tags from a given string.

    Parameters
    ----------
    html_content : str
        The input HTML content from which tags should be extracted.

    Returns
    -------
    List[str]
        A list containing all matched HTML tags (opening, closing and self‑closing).

    Notes
    -----
    - The function uses a non‑greedy regular expression to capture tags.
    - It does not raise exceptions under normal operation; if the input is
      ``None`` or an empty string, it simply returns an empty list.
    """
    if not isinstance(html_content, str):
        # Gracefully handle non‑string input
        return []

    # Regex pattern to match any HTML tag, including attributes and self‑closing tags.
    tag_pattern = re.compile(r'<[^>]+>', flags=re.DOTALL)

    # Find all non‑overlapping matches in the string
    tags = tag_pattern.findall(html_content)

    return tags