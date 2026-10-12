import re
from typing import List

# Compile the regular expression once to avoid repeated compilation overhead.
# The pattern matches any substring that starts with '<', followed by
# zero or more characters that are not '>', and ends with a '>'.
_TAG_PATTERN = re.compile(r'<[^>]*>')


def find_html_tags(html_string: str) -> List[str]:
    """
    Extract all HTML tags from the given string.

    Parameters
    ----------
    html_string : str
        The input HTML-formatted text.

    Returns
    -------
    List[str]
        A list of tag strings (including the surrounding angle brackets).
        The order of tags matches their appearance in `html_string`.

    Notes
    -----
    - This function uses a simple regular expression that is efficient for
      typical HTML content.  It does not attempt to parse malformed or deeply
      nested structures, which is adequate for most use‑cases and avoids
      catastrophic backtracking.
    - The implementation does not raise exceptions under normal operation;
      if `html_string` is not a string, it will be coerced to one.
    """
    if not isinstance(html_string, str):
        # Coerce non‑string input to string rather than raising an error.
        html_string = str(html_string)

    # Find all non‑overlapping matches of the tag pattern.
    return _TAG_PATTERN.findall(html_string)