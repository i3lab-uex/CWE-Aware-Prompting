import re
from typing import List

def get_html_tags(html_input: str) -> List[str]:
    """
    Extracts all HTML tags from the given string.

    Parameters
    ----------
    html_input : str
        The input HTML-formatted text.

    Returns
    -------
    List[str]
        A list containing all tags found in the input string.
        Each tag includes its surrounding angle brackets.

    Notes
    -----
    The implementation uses a non-greedy regular expression that matches
    any sequence of characters between '<' and the next '>' character.
    This approach is efficient, avoiding catastrophic backtracking
    (CWE-1333) and ensures that the function does not raise exceptions
    for malformed input.
    """
    if not isinstance(html_input, str):
        return []

    # Regex: match '<', then any chars except '>' (lazy), then '>'
    tag_pattern = re.compile(r'<[^>]+?>', re.IGNORECASE)

    try:
        return tag_pattern.findall(html_input)
    except Exception:
        # In the unlikely event of a regex error, return an empty list
        return []