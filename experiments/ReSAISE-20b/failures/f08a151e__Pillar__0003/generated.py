import re
from typing import List

# Compile the regex once to avoid repeated compilation overhead.
_TAG_RE = re.compile(r'<\s*\/?\s*[a-zA-Z0-9]+[^>]*>', re.IGNORECASE)

def get_html_tags(html_input: str) -> List[str]:
    """
    Extracts all HTML tags from the provided string.

    Parameters
    ----------
    html_input : str
        A string containing HTML content.

    Returns
    -------
    List[str]
        A list of tag strings found in the input.  The tags are returned
        exactly as they appear in the input, including any attributes.
        If no tags are found an empty list is returned.

    Notes
    -----
    The function never raises exceptions under normal operation.  Any
    unexpected input (e.g., ``None`` or non-string types) is safely
    converted to an empty string, and the function returns an empty list.
    """
    # Ensure we have a string to avoid errors with non-string inputs
    if not isinstance(html_input, str):
        html_input = ""

    # Find all tags; re.findall returns a list of matched strings
    try:
        tags = _TAG_RE.findall(html_input)
    except Exception:
        # In the unlikely event of a regex error, return an empty list
        tags = []

    return tags