import re
from typing import List

def find_html_tags(html_string: str) -> List[str]:
    """
    Extract all HTML tag names from the given string.

    The function uses a simple, non‑capturing regular expression that
    matches opening tags of the form <tag ...> and returns a list of the
    tag names.  It does not attempt to parse malformed or nested tags,
    and it is intentionally lightweight to avoid the worst‑case
    exponential behaviour that can arise with overly complex patterns.

    Parameters
    ----------
    html_string : str
        The HTML content to scan for tags.  If the input is not a string,
        an empty list is returned.

    Returns
    -------
    List[str]
        A list of tag names found in the input string, in order of
        appearance.  Duplicate tags are included as they occur.
    """
    if not isinstance(html_string, str):
        return []

    # Pattern explanation:
    #   <\s*          : match a '<' followed by optional whitespace
    #   ([a-zA-Z0-9]+): capture the tag name (letters or digits)
    #   [^>]*?        : non‑greedy match of any characters that are not '>'
    #   >             : the closing '>' of the tag
    #
    # The pattern is deliberately simple to avoid catastrophic backtracking.
    tag_pattern = re.compile(r'<\s*([a-zA-Z0-9]+)[^>]*?>', re.IGNORECASE)

    return tag_pattern.findall(html_string)