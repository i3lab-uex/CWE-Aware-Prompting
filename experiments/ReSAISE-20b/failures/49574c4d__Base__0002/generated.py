import re

def extract_html_elements(document: str):
    """
    Extract all HTML tags from the given document string.

    Parameters
    ----------
    document : str
        The input HTML content to be analyzed.

    Returns
    -------
    list[str]
        A list of strings, each representing an HTML tag found in the document.
        If no tags are found or an error occurs, an empty list is returned.
    """
    # Regex pattern to match any HTML tag: <...>
    # Uses a non-greedy match to avoid catastrophic backtracking.
    tag_pattern = re.compile(r"<[^>]+?>", flags=re.IGNORECASE)

    try:
        return tag_pattern.findall(document)
    except Exception:
        # In case of any unexpected error, return an empty list.
        return []