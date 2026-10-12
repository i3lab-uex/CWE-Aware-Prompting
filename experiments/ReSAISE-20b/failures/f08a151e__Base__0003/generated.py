import re
from typing import List

# Pre-compiled, non‑capturing pattern that matches opening/closing tags.
# It is deliberately simple to avoid catastrophic backtracking (CWE‑1333).
_TAG_PATTERN = re.compile(
    r'<\s*/?\s*([a-zA-Z0-9]+)(?:\s+[^>]*?)?>',
    re.IGNORECASE
)

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
        A list of tag names (without angle brackets or attributes) found in the
        input string.  Duplicate tags are preserved in the order of appearance.

    Notes
    -----
    - The function is defensive: it returns an empty list if the input is not
      a string or is ``None``.
    - The regex used avoids catastrophic backtracking by not employing
      nested quantifiers or look‑behind constructs.
    """
    if not isinstance(html_input, str):
        return []

    # Find all matches; group 1 captures the tag name.
    tags = [_match.group(1) for _match in _TAG_PATTERN.finditer(html_input)]
    return tags