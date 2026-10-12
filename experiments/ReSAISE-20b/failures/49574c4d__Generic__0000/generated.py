import re
from typing import List

def extract_html_elements(document: str) -> List[str]:
    """
    Return a list of all substrings in `document` that look like HTML tags.
    
    The function uses a non‑greedy regular expression to match anything
    that starts with '<', ends with '>', and contains at least one non‑'>'
    character.  This includes start tags, end tags, self‑closing tags,
    and even comment blocks (e.g. <!-- ... -->).  The function never
    raises an exception – if the input is not a string it will simply
    return an empty list.
    
    Parameters
    ----------
    document : str
        The HTML content to scan for tags.

    Returns
    -------
    List[str]
        A list of tag strings in the order they appear in `document`.
    """
    if not isinstance(document, str):
        return []

    # Regex explanation:
    #   <            : literal '<'
    #   \s*          : optional whitespace after the opening bracket
    #   (?:/)?       : optional leading slash for closing tags
    #   [^>]+?       : one or more characters that are not '>', non‑greedy
    #   >            : literal '>'
    tag_pattern = re.compile(r'<\s*(?:/)?[^>]+?>', re.IGNORECASE | re.DOTALL)

    return tag_pattern.findall(document)