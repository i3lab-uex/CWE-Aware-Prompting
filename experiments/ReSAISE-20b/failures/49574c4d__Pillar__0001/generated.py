import re
from typing import List

def extract_html_elements(document: str) -> List[str]:
    """
    Extracts all HTML tags from the provided document string.

    Parameters
    ----------
    document : str
        The input HTML content to be analyzed.

    Returns
    -------
    List[str]
        A list containing the matched HTML tags as strings.
    """
    if not isinstance(document, str):
        # Gracefully handle non-string input
        return []

    # Regular expression to match opening and closing tags.
    # It matches:
    #   <tag ...>
    #   </tag>
    # and allows for optional attributes, whitespace, and self-closing tags.
    tag_pattern = re.compile(
        r'<\s*\/?\s*[a-zA-Z][^\s>]*[^>]*>',
        re.IGNORECASE
    )

    try:
        matches = tag_pattern.findall(document)
        return matches
    except re.error:
        # In the unlikely event of a regex compilation/runtime error,
        # return an empty list to avoid raising exceptions.
        return []