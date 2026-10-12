import re

def extract_html_elements(document: str) -> list[str]:
    """
    Return a list of all HTML tags found in the given document string.

    Parameters
    ----------
    document : str
        The input HTML content to analyze.

    Returns
    -------
    list[str]
        A list of strings, each string being an HTML tag (e.g., "<div>", "</p>",
        "<img src='...'>").
    """
    # Ensure the input is a string; if not, convert it to an empty string.
    try:
        text = str(document)
    except Exception:
        return []

    # Regular expression to match anything that starts with '<' and ends with '>'
    # but does not contain a newline inside the tag. This is a simple pattern
    # suitable for most typical HTML snippets.
    tag_pattern = re.compile(r'<[^>\s]+(?:\s+[^>]+)?/>|<[^>]*?>', re.DOTALL)

    # Find all matches; if none, return an empty list.
    tags = tag_pattern.findall(text)
    return tags