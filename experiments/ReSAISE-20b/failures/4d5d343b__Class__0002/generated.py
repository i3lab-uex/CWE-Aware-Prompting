import re

# Compile a simple, efficient regex to capture HTML tags.
# The pattern matches a '<' followed by any characters that are not '>' (non-greedy)
# until the next '>'. This avoids catastrophic backtracking because it never
# consumes a '>' character inside the tag.
_TAG_RE = re.compile(r'<[^>]+>', flags=re.UNICODE)


def grab_html_tags(html_code: str) -> list[str]:
    """
    Scan the supplied string for HTML tags and return them as a list.

    Parameters
    ----------
    html_code : str
        The HTML string to parse. If ``None`` or an empty string, an empty list is returned.

    Returns
    -------
    list[str]
        A list of all tags found in the input string, preserving their order.

    Notes
    -----
    - The function uses a pre‑compiled regular expression to avoid repeated compilation.
    - The regex is deliberately simple and does not attempt to parse nested tags or malformed
      markup; it merely finds substrings that look like tags.
    - No exceptions are raised for malformed input – the function simply returns an empty
      list when appropriate.
    """
    if not html_code:
        return []

    # Use findall to retrieve all non-overlapping matches.
    # The result will be a list of strings containing the tags exactly as they appear.
    return _TAG_RE.findall(html_code)