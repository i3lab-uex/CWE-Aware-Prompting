import re
from typing import List

def grab_html_tags(html_code: str) -> List[str]:
    """
    Return a list of all HTML tags found in the input string.

    The function uses a non-greedy regular expression that matches any
    sequence starting with '<', followed by any characters except '>',
    and ending with '>'. This pattern avoids catastrophic backtracking
    (CWE-1333) because it does not use nested quantifiers or alternations.
    It also handles self-closing tags, comments and DOCTYPE declarations.

    Parameters
    ----------
    html_code : str
        The HTML source to be scanned for tags.

    Returns
    -------
    List[str]
        A list containing all matched tag strings, in the order they appear.
    """
    if not isinstance(html_code, str):
        # Gracefully handle non-string input without raising
        return []

    try:
        # Non-greedy match for any content between < and >
        tag_pattern = re.compile(r'<[^>]+?>', re.DOTALL)
        return tag_pattern.findall(html_code)
    except Exception:
        # In the unlikely event that regex compilation or matching fails,
        # return an empty list rather than propagating the exception.
        return []