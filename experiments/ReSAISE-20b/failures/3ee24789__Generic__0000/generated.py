import re
from typing import List

def detect_html_tags(html_str: str) -> List[str]:
    """
    Return a list of all HTML tags found in the input string.

    Parameters
    ----------
    html_str : str
        The HTML content to search for tags.

    Returns
    -------
    List[str]
        A list of tag strings, e.g. ['<div>', '<img src="x">', '</p>'].
    """
    # Compile a non‑greedy pattern that matches anything between < and >
    tag_pattern = re.compile(r'<[^>]+?>')
    # Find all matches; return an empty list if none are found
    return tag_pattern.findall(html_str) or []