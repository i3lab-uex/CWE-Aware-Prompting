import re

def extract_html_tags(html_string: str) -> list[str]:
    """
    Extract all HTML tags from the provided string.

    Parameters
    ----------
    html_string : str
        The input HTML content to parse.

    Returns
    -------
    list[str]
        A list of all tag strings found in the input. If no tags are
        present, an empty list is returned.
    """
    if not isinstance(html_string, str):
        # Gracefully handle non‑string inputs
        return []

    # Regular expression to match an opening or closing tag,
    # including self‑closing tags and attributes.
    # The pattern is intentionally non‑greedy to avoid overmatching.
    tag_pattern = re.compile(r'<[^>]+?>', flags=re.IGNORECASE)

    try:
        # Find all non‑overlapping matches
        return tag_pattern.findall(html_string)
    except re.error:
        # In the unlikely event of a regex compilation/runtime error,
        # return an empty list instead of propagating the exception.
        return []