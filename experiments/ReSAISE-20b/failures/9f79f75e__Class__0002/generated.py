import re
from typing import List

# Compile the regex once to avoid repeated compilation overhead.
_TAG_RE = re.compile(r'<[^>]*?>', flags=re.IGNORECASE | re.DOTALL)


def find_html_tags(html_string: str) -> List[str]:
    """
    Extract all HTML tags from the given string.

    Parameters
    ----------
    html_string : str
        The input HTML-formatted text.

    Returns
    -------
    List[str]
        A list of all tags found in the input string, preserving their order.
        Tags include the surrounding angle brackets, e.g. '<div>' or '</p>'.
    """
    if not isinstance(html_string, str):
        # Gracefully handle non-string input by converting to string.
        html_string = str(html_string)

    # re.findall returns an empty list if no matches are found.
    return _TAG_RE.findall(html_string)