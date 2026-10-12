import re

def detect_html_tags(html_str: str):
    """
    Detect all HTML tags in the provided string.

    Parameters
    ----------
    html_str : str
        The input HTML content to be analyzed.

    Returns
    -------
    list[str]
        A list of strings, each representing an HTML tag found in the input.
        The tags are returned exactly as they appear (including angle brackets).

    Notes
    -----
    - The function uses a simple regular expression that matches any substring
      starting with '<' and ending with '>' without crossing nested tags.
    - No exceptions are raised; invalid input is treated as an empty string.
    """
    if not isinstance(html_str, str):
        # Defensive: treat non-string input as empty
        return []

    # Regular expression to capture tags:
    #   < followed by optional whitespace, optional '/' for closing tags,
    #   one or more word characters (tag name), then any non-'>' characters
    #   and finally a closing '>'.
    tag_pattern = re.compile(r'<\s*/?\s*\w[^>]*?>', re.IGNORECASE)

    # Find all non-overlapping matches
    tags = tag_pattern.findall(html_str)
    return tags