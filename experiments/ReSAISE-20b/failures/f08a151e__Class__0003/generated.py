import re
from typing import List

# Regular expression that matches simple HTML tags.
# It captures opening, closing and self‑closing tags without trying to parse attributes
_TAG_RE = re.compile(
    r'<\s*'                 # opening <
    r'/?'                   # optional /
    r'\s*([a-zA-Z0-9]+)'    # tag name (captured)
    r'(?:\s+[^>]*)?'        # optional attributes
    r'\s*/?\s*>'             # optional / and closing >
', re.IGNORECASE)

def get_html_tags(html_input: str) -> List[str]:
    """
    Extracts all HTML tags from the provided string.

    Parameters
    ----------
    html_input : str
        The input string containing HTML markup.

    Returns
    -------
    List[str]
        A list of tag names (without angle brackets or attributes) that appear
        in the input string, preserving order of first appearance.

    Notes
    -----
    - The function uses a simple regular expression that is safe from
      catastrophic backtracking (no nested or recursive patterns).
    - It ignores malformed tags; only well‑formed tags that match the pattern
      are returned.
    - No exception is raised for normal input; malformed or empty strings simply
      yield an empty list.
    """
    if not isinstance(html_input, str):
        # If the input is not a string we return an empty list.
        return []

    # Find all matches and extract the captured tag names.
    tags = [_match.group(1) for _match in _TAG_RE.finditer(html_input)]
    return tags