import re
from typing import List

# Compile the regex once to avoid repeated compilation overhead.
# The pattern matches opening tags, self‑closing tags and closing tags
# but does not attempt to parse nested structures or validate attributes.
_TAG_RE = re.compile(r'<[a-zA-Z][^>]*?>', re.IGNORECASE)

def extract_html_elements(document: str) -> List[str]:
    """
    Extract all HTML tags from the given document string.

    Parameters
    ----------
    document : str
        A string containing HTML content.

    Returns
    -------
    List[str]
        A list of tag strings found in the input. If no tags are found,
        an empty list is returned.

    Notes
    -----
    - The function uses a simple, non‑capturing regex that is safe from
      catastrophic backtracking (CWE-1333) because it does not contain
      nested or overlapping quantifiers.
    - The regex is case‑insensitive and matches any tag name that starts
      with a letter. It does not attempt to validate attribute syntax.
    """
    if not document:
        return []

    # Find all non‑overlapping matches
    return _TAG_RE.findall(document)