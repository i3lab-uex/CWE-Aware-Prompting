import re
from typing import List

# Pre‑compiled regex that matches HTML tags in a safe, non‑backtracking way.
# It captures the tag name (letters, digits, hyphen or colon) and ignores
# attributes and closing slashes.  The pattern is deliberately simple to avoid
# catastrophic backtracking (CWE‑407).
_TAG_RE = re.compile(r'<\s*/?\s*([a-zA-Z0-9:-]+)[^>]*?>', re.IGNORECASE)


def get_html_tags(html_input: str) -> List[str]:
    """
    Extract all HTML tag names from the given string.

    Parameters
    ----------
    html_input : str
        A string containing HTML content.

    Returns
    -------
    List[str]
        A list of tag names found in the input, in the order they appear.
        Duplicate tags are preserved.

    Notes
    -----
    - The function is tolerant of malformed HTML and will simply ignore any
      fragments that do not match the expected pattern.
    - It does not raise exceptions for normal input; any unexpected error
      will be caught and an empty list returned to maintain safety.
    """
    try:
        # Find all matches; each match's group(1) is the tag name.
        return [m.group(1).lower() for m in _TAG_RE.finditer(html_input)]
    except Exception:
        # In the unlikely event of an exception (e.g., bad regex or
        # non‑string input), return an empty list to avoid breaking callers.
        return []