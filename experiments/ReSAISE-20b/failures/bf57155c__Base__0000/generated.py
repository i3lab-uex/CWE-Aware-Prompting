import re

def identify_html_tags(content: str) -> list[str]:
    """
    Scan the input string for HTML tags and return a list of all detected tags.

    Parameters
    ----------
    content : str
        The HTML string to parse.

    Returns
    -------
    list[str]
        A list containing each matched HTML tag as a string. If no tags are found,
        an empty list is returned.

    Notes
    -----
    * The regular expression used is intentionally simple and non‑capturing
      to avoid the risk of catastrophic backtracking (CWE‑1333). It matches any
      opening `<` followed by one or more characters that are not `>`, and then a
      closing `>`.

    * The function is defensive: it returns an empty list if the input is not a
      string or if any unexpected error occurs during matching, thereby never
      raising an exception.

    Examples
    --------
    >>> identify_html_tags('<div><p>Hello</p></div>')
    ['<div>', '<p>', '</p>', '</div>']
    """
    if not isinstance(content, str):
        return []

    # Simple non‑capturing pattern that matches any tag without greedily
    # consuming across multiple tags.
    TAG_PATTERN = re.compile(r'<[^>]+>', flags=re.DOTALL)

    try:
        return TAG_PATTERN.findall(content)
    except Exception:
        # In case of any unforeseen error, fall back to an empty list.
        return []