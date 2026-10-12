import re
from typing import List

# Pre‑compile a safe, non‑greedy pattern that matches HTML tags.
# The pattern captures:
#   - a leading '<'
#   - optional whitespace and an optional '/' for closing tags
#   - the tag name (sequence of non‑space, non-> characters)
# It does not attempt to parse attributes or nested tags.
_TAG_PATTERN = re.compile(r'<\s*/?\s*([^\s>]+)', flags=re.IGNORECASE)


def get_html_tags(html_input: str) -> List[str]:
    """
    Extract all HTML tag names from the provided string.

    Parameters
    ----------
    html_input : str
        A string containing HTML content.

    Returns
    -------
    List[str]
        A list of tag names found in the input. Tag names are returned
        without angle brackets or any leading '/'.

    Notes
    -----
    - The function is tolerant to malformed input and will never raise.
    - It intentionally ignores attributes, self‑closing slashes, and
      comments to keep the regex simple and efficient.
    """
    if not isinstance(html_input, str):
        # Gracefully handle non‑string input
        return []

    # Find all matches; each match is a tuple with the tag name.
    tags = [match[0] for match in _TAG_PATTERN.findall(html_input)]
    return tags