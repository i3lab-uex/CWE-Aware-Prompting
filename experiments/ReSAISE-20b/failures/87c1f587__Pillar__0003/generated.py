import re

def find_html_tags(html_content: str) -> list[str]:
    """
    Return a list of all HTML tags found in the input string.

    Parameters
    ----------
    html_content : str
        The HTML content to be searched for tags.

    Returns
    -------
    list[str]
        A list of strings, each string being a matched HTML tag.
    """
    if not isinstance(html_content, str):
        # Gracefully handle non-string input by returning an empty list
        return []

    # Regular expression to match opening, closing, self-closing tags,
    # and comments. It is intentionally simple to avoid excessive
    # backtracking or catastrophic cases.
    tag_pattern = re.compile(r'<[^>]+?>')

    # Find all non-overlapping matches in the string
    tags = tag_pattern.findall(html_content)

    return tags