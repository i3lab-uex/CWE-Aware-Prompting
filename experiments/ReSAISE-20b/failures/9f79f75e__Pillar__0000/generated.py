import re
from typing import List

def find_html_tags(html_string: str) -> List[str]:
    """
    Extract all HTML tags from a string.

    Parameters
    ----------
    html_string : str
        A string containing HTML content.

    Returns
    -------
    List[str]
        A list of tags found in the input string. If no tags are found,
        an empty list is returned.

    Notes
    -----
    - The function is tolerant to malformed input: if `html_string` is
      not a string or is ``None`` it returns an empty list instead of
      raising an exception.
    - The regex used matches any sequence that starts with '<' and ends
      with '>' without crossing newlines. It does not attempt to validate
      HTML structure or handle comments, CDATA sections, etc.
    """
    if not isinstance(html_string, str):
        return []

    # Pattern matches anything that starts with '<', followed by any
    # characters except '>' (non-greedy), and ends with '>'.
    tag_pattern = re.compile(r'<[^>]+?>', re.DOTALL)

    # Find all non-overlapping matches
    return tag_pattern.findall(html_string)