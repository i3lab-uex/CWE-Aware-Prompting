import re

# Pre‑compiled regular expression that matches any HTML tag.
# The pattern uses a negated character class to avoid greedy matching
# and ensures that the search is linear in the input size.
_TAG_RE = re.compile(r'<[^>]+>', flags=re.IGNORECASE | re.DOTALL)

def parse_html_tags(html: str) -> list[str]:
    """
    Extract all HTML tags from the given string.

    Parameters
    ----------
    html : str
        The input HTML string to be parsed.

    Returns
    -------
    list[str]
        A list of all tags found in the input string.  Each tag includes
        the surrounding angle brackets (e.g., "<div>", "</a>", "<br/>").
    """
    if not isinstance(html, str):
        # Gracefully handle non‑string input by returning an empty list.
        return []

    # `findall` returns all non‑overlapping matches of the pattern.
    return _TAG_RE.findall(html)