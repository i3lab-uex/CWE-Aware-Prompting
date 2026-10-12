import re
from typing import List

def extract_html_tags(html_string: str) -> List[str]:
    """
    Extract all HTML tags from the provided string using a safe regular expression.

    Parameters
    ----------
    html_string : str
        The HTML content to parse.

    Returns
    -------
    List[str]
        A list of all tags found in the input string.  If the input is not a
        string or an error occurs during matching, an empty list is returned.
    """
    if not isinstance(html_string, str):
        return []

    # A non-greedy pattern that matches anything between < and >, avoiding
    # catastrophic backtracking by limiting the character set to all but '>'.
    tag_pattern = re.compile(r'<[^>]+?>', flags=re.IGNORECASE)

    try:
        return tag_pattern.findall(html_string)
    except re.error:  # pragma: no cover
        # In the unlikely event that the regex compilation fails,
        # return an empty list instead of raising.
        return []