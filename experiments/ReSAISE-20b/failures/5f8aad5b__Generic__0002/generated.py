import re
from typing import List

def extract_html_tags(html_content: str) -> List[str]:
    """
    Extracts the names of all HTML tags present in a string.

    Parameters
    ----------
    html_content : str
        A string containing HTML markup.

    Returns
    -------
    List[str]
        A list of tag names (without angle brackets or attributes) in the order they appear.
    """
    if not isinstance(html_content, str):
        # Gracefully handle non‑string input by returning an empty list
        return []

    try:
        # Matches tags like <div>, </span>, <a href="...">, etc.
        tag_pattern = re.compile(r'<\s*/?\s*([a-zA-Z0-9]+)[^>]*>', re.IGNORECASE)
        tags = tag_pattern.findall(html_content)
        return tags
    except Exception:
        # In the unlikely event of an unexpected error, return an empty list
        return []