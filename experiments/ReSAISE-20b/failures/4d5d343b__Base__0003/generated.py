import re
from typing import List

def grab_html_tags(html_code: str) -> List[str]:
    """
    Return a list of all HTML tags found in *html_code*.

    The function uses a non‑capturing regex that matches any substring
    starting with '<', followed by one or more characters that are not
    '>', and ending with '>'.  This pattern is linear in the length of
    *html_code* and does not suffer from exponential backtracking.

    Parameters
    ----------
    html_code : str
        The HTML string to parse.

    Returns
    -------
    List[str]
        A list of all tags (including the surrounding angle brackets).
    """
    if not isinstance(html_code, str):
        return []

    # Compile the regex once to avoid re‑compilation on each call.
    tag_pattern = re.compile(r'<[^>]+>', flags=re.DOTALL)

    # Find all non‑overlapping matches.
    return tag_pattern.findall(html_code)