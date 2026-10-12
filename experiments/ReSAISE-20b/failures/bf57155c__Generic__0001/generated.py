import re

def identify_html_tags(content: str) -> list[str]:
    """
    Scan the provided HTML string and return a list of all tags found.

    Parameters
    ----------
    content : str
        The HTML string to parse.

    Returns
    -------
    list[str]
        A list containing each tag (including angle brackets) in the order
        they appear. If no tags are found, an empty list is returned.
    """
    try:
        # Use a non-greedy match to capture individual tags
        return re.findall(r'<[^>]*?>', content)
    except Exception:
        # In case of any unexpected error, return an empty list
        return []