import re
from typing import List

def grab_html_tags(html_code: str) -> List[str]:
    """
    Scan the provided HTML string for tags and return a list of all detected tag names.

    Parameters
    ----------
    html_code : str
        The HTML source to be parsed.

    Returns
    -------
    List[str]
        A list containing the names of all tags found in ``html_code``.
        If no tags are present, an empty list is returned.

    Notes
    -----
    * The function uses a regular expression that captures the tag name part of an HTML
      element. It does **not** attempt to fully validate or parse nested tags; it simply
      returns all tag names that appear in the input string.
    * The implementation is defensive: any exception raised during regex matching
      (for example, if ``html_code`` is not a string) will be caught and an empty list
      will be returned, ensuring the function never propagates errors.
    * The regex deliberately allows for optional whitespace and an optional leading
      slash (for closing tags). It does not capture attributes; only the tag name.
    """
    if not isinstance(html_code, str):
        # If input is not a string we return an empty list to avoid raising.
        return []

    try:
        # Pattern matches <tag>, </tag>, <tag ...> etc. and captures the tag name.
        pattern = re.compile(r'<\s*/?\s*([a-zA-Z0-9:-]+)[^>]*>', re.IGNORECASE)
        tags = pattern.findall(html_code)
        return tags
    except Exception:
        # Any unexpected error results in an empty list.
        return []