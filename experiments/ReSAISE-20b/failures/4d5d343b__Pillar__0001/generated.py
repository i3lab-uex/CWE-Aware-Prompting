import re
from typing import List

def grab_html_tags(html_code: str) -> List[str]:
    """
    Scan the provided string for HTML tags using a regular expression
    and return a list containing all detected tags.

    Parameters:
        html_code (str): The HTML string to parse.

    Returns:
        List[str]: A list of all matched tags. If no tags are found,
                   an empty list is returned.

    Notes:
        - The function never raises exceptions; invalid input such as
          None or non-string values is safely handled.
        - The regex pattern captures any substring that starts with '<',
          contains characters other than '>' until the next '>', and
          ends with a '>'. It does not attempt to validate tag names
          or attributes.
    """
    # Guard against non-string inputs
    if not isinstance(html_code, str):
        return []

    # Regular expression to match HTML tags (including self-closing and comments)
    tag_pattern = r'<[^>]+>'
    try:
        tags = re.findall(tag_pattern, html_code)
    except Exception:
        # In the unlikely event of a regex error, return an empty list
        tags = []

    return tags