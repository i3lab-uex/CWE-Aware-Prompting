import re

# Compile the regular expression once to avoid repeated compilation overhead.
_TAG_PATTERN = re.compile(r'<[^>]+>')

def detect_html_tags(html_str: str) -> list[str]:
    """
    Detect all HTML tags in the provided string.

    Parameters
    ----------
    html_str : str
        The input HTML content to analyze.

    Returns
    -------
    list[str]
        A list of strings, each string being an HTML tag found in the input.
    """
    # Guard against None input and non-string types.
    if not isinstance(html_str, str):
        return []

    # Find all substrings that match the pattern for an HTML tag.
    tags = _TAG_PATTERN.findall(html_str)

    # Return a new list to avoid accidental mutation of internal data.
    return list(tags)