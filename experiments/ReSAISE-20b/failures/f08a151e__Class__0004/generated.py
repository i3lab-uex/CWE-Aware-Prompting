import re

def get_html_tags(html_input: str) -> list[str]:
    """
    Extract all HTML tags from the provided string.

    Parameters
    ----------
    html_input : str
        A string containing HTML content.

    Returns
    -------
    list[str]
        A list of tag strings found in the input.  The tags include
        opening, closing, and self‑closing forms (e.g., <div>, </p>,
        <img src="..."/>).  The function is tolerant of malformed
        markup and will not raise an exception for ordinary inputs.

    Notes
    -----
    The regular expression used is intentionally simple and efficient,
    avoiding catastrophic backtracking by employing a non‑greedy match
    (`?`) and limiting the character set for tag names to alphanumerics.
    """
    # Pattern explanation:
    #   <\s*            : match the opening '<' followed by optional whitespace
    #   /?              : optionally match a '/' for closing tags
    #   \s*             : optional whitespace after the '/'
    #   [a-zA-Z0-9]+    : tag name (alphanumeric only)
    #   [^>]*?          : any characters except '>' lazily (attributes, etc.)
    #   >               : closing '>'
    tag_pattern = re.compile(r'<\s*/?\s*[a-zA-Z0-9]+[^>]*?>', re.IGNORECASE)

    # Find all non‑overlapping matches
    tags = tag_pattern.findall(html_input)
    return tags