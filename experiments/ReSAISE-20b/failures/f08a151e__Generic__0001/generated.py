import re
from typing import List

def get_html_tags(html_input: str) -> List[str]:
    """
    Extracts all HTML tags from the provided string.

    Parameters
    ----------
    html_input : str
        A string containing HTML markup.

    Returns
    -------
    List[str]
        A list of tag strings, each including the surrounding angle brackets.
        Tags are returned in the order they appear in the input.

    Notes
    -----
    * The function uses a non-greedy regular expression to match any substring
      that starts with '<', ends with '>', and does not contain a '>' in between.
    * It is tolerant of malformed markup; it will simply return the longest
      substrings that match the pattern.
    * No exceptions are raised during normal operation; any unexpected input
      (e.g., non-string) will be converted to a string before processing.
    """
    # Ensure the input is a string; if not, convert it safely
    try:
        text = str(html_input)
    except Exception:  # pragma: no cover
        return []

    # Regular expression to match HTML tags:
    #   - '<' followed by any characters except '>' (non-greedy)
    #   - '>'
    tag_pattern = re.compile(r'<[^>]+?>', flags=re.DOTALL)

    # Find all non-overlapping matches
    tags = tag_pattern.findall(text)

    return tags