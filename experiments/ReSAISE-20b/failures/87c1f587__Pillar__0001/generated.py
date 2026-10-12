import re
from typing import List

def find_html_tags(html_content: str) -> List[str]:
    """
    Return a list of all substrings that look like HTML tags in the given input.

    A tag is defined as a '<' character followed by any characters that are not
    '>' and ending with a '>'. This simple pattern captures most common tags,
    including self‑closing ones (e.g., <br/>) and comments (e.g., <!-- comment -->).
    It does not perform full HTML validation.

    Parameters
    ----------
    html_content : str
        The string to search for tags in.

    Returns
    -------
    List[str]
        A list of matched tag strings. If no tags are found, an empty list is returned.
    """
    if not isinstance(html_content, str):
        # If the input is not a string, return an empty list instead of raising.
        return []

    # Regular expression to match HTML tags:
    #   <          : opening angle bracket
    #   [^>]*      : any number of characters that are not '>'
    #   >          : closing angle bracket
    pattern = r'<[^>]*>'
    try:
        tags = re.findall(pattern, html_content)
    except re.error:
        # In the unlikely event that the regex compilation fails,
        # return an empty list rather than propagating an exception.
        tags = []

    return tags