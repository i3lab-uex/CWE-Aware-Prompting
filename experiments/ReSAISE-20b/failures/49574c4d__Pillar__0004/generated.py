import re

def extract_html_elements(document: str) -> list[str]:
    """
    Return a list of all HTML tags found in the given document string.

    The function uses a regular expression that matches opening and closing
    tags, self‑closing tags, and any attributes within them.  It is deliberately
    conservative: it does not attempt to validate the syntax of attributes or
    nested structure; it simply captures any sequence that starts with '<',
    contains any characters except '>', and ends with '>'.

    Parameters
    ----------
    document : str
        The HTML content to search.

    Returns
    -------
    list[str]
        A list of matched tag strings in the order they appear.
    """
    # Regular expression that matches any HTML tag:
    #   - '<' followed by zero or more characters that are not '>'
    #   - ending with '>'
    tag_pattern = re.compile(r'<[^>]+>')
    try:
        return tag_pattern.findall(document)
    except Exception:  # pragma: no cover
        # In case of any unforeseen error, return an empty list to satisfy the
        # requirement that no exception is raised.
        return []