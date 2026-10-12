import re

# Compile the regex once for efficiency and to avoid repeated compilation overhead.
# The pattern matches a '<', followed by any number of characters that are not '>',
# and then a closing '>'. It is deliberately simple to avoid catastrophic
# backtracking attacks (CWE-407).
_TAG_RE = re.compile(r'<[^>]+>', flags=re.IGNORECASE)

def parse_html_tags(html: str) -> list[str]:
    """
    Extract all HTML tags from the input string.

    Parameters
    ----------
    html : str
        The input HTML content.

    Returns
    -------
    list[str]
        A list containing each matched tag as a string.
    """
    if not isinstance(html, str):
        # Gracefully handle non-string inputs by returning an empty list.
        return []

    # re.findall returns a list of all non-overlapping matches in the string.
    return _TAG_RE.findall(html)