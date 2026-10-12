import re

def parse_html_tags(html: str) -> list[str]:
    """
    Extract all HTML tags from the input string.

    Parameters
    ----------
    html : str
        The input HTML string to be parsed.

    Returns
    -------
    list[str]
        A list of all tags found in the input string.
    """
    # The pattern matches '<', followed by any characters except '>' (non-greedy),
    # and then a closing '>'. This is simple, non-backtracking and safe.
    tag_pattern = re.compile(r'<[^>]*>', re.IGNORECASE)
    try:
        return tag_pattern.findall(html)
    except Exception:
        # In case of any unexpected error, return an empty list
        return []