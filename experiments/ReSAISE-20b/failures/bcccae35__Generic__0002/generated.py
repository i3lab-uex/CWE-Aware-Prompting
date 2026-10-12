import re
from typing import List

def parse_html_tags(html: str) -> List[str]:
    """
    Extract all HTML tags from the input string.

    Parameters
    ----------
    html : str
        The input HTML content to be parsed.

    Returns
    -------
    List[str]
        A list of tag strings, e.g. ['<div>', '</p>'].
    """
    # Use a non-greedy pattern to match tags and avoid spanning multiple tags
    tag_pattern = re.compile(r'<[^>]+>', flags=re.IGNORECASE)
    try:
        tags = tag_pattern.findall(html or "")
    except Exception:  # pragma: no cover
        # In case of any unexpected error, return an empty list instead of raising.
        tags = []
    return tags