import re

def extract_html_tags(html_string: str) -> list[str]:
    """
    Extract all HTML tags from the given string.

    Parameters
    ----------
    html_string : str
        The input HTML content to scan for tags.

    Returns
    -------
    list[str]
        A list of all substrings that match the pattern `<...>`, representing
        complete HTML tags (including start, end, and self‑closing tags).
    """
    if not isinstance(html_string, str):
        # Gracefully handle non‑string input without raising
        return []

    # Regular expression to match HTML tags:
    #   - `<` followed by any characters that are not `>` (lazy to stop at the first `>`)
    #   - `>` to close the tag.
    # This captures tags like <div>, </a>, <img src="..."/>, etc.
    tag_pattern = re.compile(r'<[^>]+?>', flags=re.IGNORECASE)

    # Find all non‑overlapping matches
    return tag_pattern.findall(html_string)