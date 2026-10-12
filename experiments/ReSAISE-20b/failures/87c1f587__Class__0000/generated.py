import re
from typing import List

def find_html_tags(html_content: str) -> List[str]:
    """
    Return a list of all HTML tags found in `html_content`.

    The function uses a simple, non-backtracking regular expression
    that matches an opening angle bracket '<', followed by any
    characters except '>' (including whitespace and attributes), and
    terminated by a closing angle bracket '>'.  This pattern is
    efficient for typical HTML input and avoids the pitfalls of
    catastrophic backtracking.

    Parameters
    ----------
    html_content : str
        The string containing HTML to be parsed.

    Returns
    -------
    List[str]
        A list of strings, each representing a matched HTML tag.
    """
    # Pattern: < followed by any characters except '>' (non-greedy), then >
    tag_pattern = re.compile(r"<[^>]+>", flags=re.IGNORECASE)

    # Find all non-overlapping matches
    return tag_pattern.findall(html_content)