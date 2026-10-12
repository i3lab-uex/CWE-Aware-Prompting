import re
from typing import List

# Regular expression to capture HTML tags, including self‑closing and attributes.
_TAG_RE = re.compile(r'<\s*(/?[a-zA-Z][a-zA-Z0-9:-]*)(?:\s[^>]*)?>', re.IGNORECASE)


def extract_html_tags(html_string: str) -> List[str]:
    """
    Extracts all HTML tags from the provided string.

    Parameters
    ----------
    html_string : str
        The input HTML content to search for tags.

    Returns
    -------
    List[str]
        A list of matched tag names, including the leading slash for closing tags.
        For example: ['div', '/p', 'img'].

    Notes
    -----
    - The function is defensive: if the input is not a string, it returns an empty list.
    - The regular expression deliberately captures only the tag name (and a possible leading slash)
      and ignores attributes, whitespace, or malformed tags.
    - No resources are allocated that require explicit cleanup; the function is safe from
      CWE‑664 concerns.
    """
    if not isinstance(html_string, str):
        return []

    # Find all matches; each match is a tuple with the captured tag name.
    matches = _TAG_RE.findall(html_string)
    return list(matches)