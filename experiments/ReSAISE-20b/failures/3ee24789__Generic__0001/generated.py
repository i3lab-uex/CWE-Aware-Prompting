import re

def detect_html_tags(html_str: str) -> list[str]:
    """
    Find all HTML tags in the given string using a regular expression.

    Parameters
    ----------
    html_str : str
        Input string containing potential HTML markup.

    Returns
    -------
    list[str]
        A list of matched tag strings. If no tags are found, an empty list is returned.
    """
    if not isinstance(html_str, str):
        # Gracefully handle non-string input by returning an empty list
        return []

    # Regex to match opening, closing and self‑closing tags.
    # It deliberately excludes comments (<!-- ... -->) and DOCTYPE declarations.
    tag_pattern = re.compile(
        r'<(?P<tag_name>[A-Za-z][A-Za-z0-9]*)'          # tag name
        r'(?:\s+[^<>]*?)?'                            # optional attributes
        r'(?P<self_close>\s*/)?>'                     # optional self‑closing slash
        r'|</(?P<close_tag_name>[A-Za-z][A-Za-z0-9]*)\s*>'  # closing tags
    )

    matches = []
    for m in tag_pattern.finditer(html_str):
        # Exclude DOCTYPE and other declarations
        if m.group('tag_name') is None and m.group('close_tag_name') is None:
            continue
        # Reconstruct the full tag string from the match span
        matches.append(html_str[m.start():m.end()])

    return matches