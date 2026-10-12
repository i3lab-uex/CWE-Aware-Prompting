import re
from typing import List

# Regular expression to match simple HTML tags.
# It captures opening, closing and self‑closing tags without excessive backtracking.
_TAG_RE = re.compile(
    r'<\s*/?\s*'          # '<', optional '/', optional whitespace
    r'[a-zA-Z][^>\s]*'    # tag name (first character alphabetic)
    r'(?:\s+[^>]*)?'      # optional attributes
    r'\s*/?>',            # optional '/' before '>' and closing '>'
    re.IGNORECASE | re.DOTALL
)

def identify_html_tags(content: str) -> List[str]:
    """
    Scan the given string for HTML tags using a regular expression and return
    all matched tags.

    Parameters:
        content (str): The input string containing potential HTML markup.

    Returns:
        List[str]: A list of matched tag strings. Empty if none are found.
    """
    try:
        # Ensure the input is a string; otherwise return empty list
        if not isinstance(content, str):
            return []

        # Find all non-overlapping matches of the tag pattern
        tags = _TAG_RE.findall(content)
        return tags

    except Exception:
        # Any unexpected error is swallowed to keep the function exception‑free
        return []