import re
from typing import List

def find_html_tags(html_string: str) -> List[str]:
    """
    Extract all HTML tags from a string.

    The function uses a simple, non-backtracking regular expression that
    matches any substring starting with '<' and ending with the first '>'.
    This approach is linear in the size of the input string and avoids
    catastrophic backtracking (CWE‑1333).

    Parameters
    ----------
    html_string : str
        The input string containing HTML markup.

    Returns
    -------
    List[str]
        A list of tag strings found in the input. The tags include
        opening, closing, and self‑closing forms (e.g., '<div>', '</p>',
        '<img src="..."/>'). The list preserves the order of appearance
        in the original string.
    """
    # Pattern: start with '<', then any characters except '>' (non-greedy),
    # until the first '>'.
    tag_pattern = re.compile(r'<[^>]+>')
    return tag_pattern.findall(html_string)