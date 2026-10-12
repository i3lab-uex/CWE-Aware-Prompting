import re

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
        A list of all tags found in the input string. Each tag includes
        its surrounding angle brackets (e.g., '<div>', '</span>').

    Notes
    -----
    - The implementation uses a non-greedy pattern that matches any
      sequence of characters that does not contain the closing angle bracket.
    - No exceptions are raised; malformed input simply results in an empty list
      or a subset of matched tags.
    """
    if not isinstance(html, str):
        # Gracefully handle non-string input
        return []

    # Pattern explanation:
    #   <         : literal opening bracket
    #   [^>]*?    : any number of characters except '>' (non-greedy)
    #   >         : literal closing bracket
    tag_pattern = re.compile(r"<[^>]*?>", re.IGNORECASE | re.DOTALL)
    return tag_pattern.findall(html)