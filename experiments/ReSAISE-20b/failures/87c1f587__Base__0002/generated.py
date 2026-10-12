import re
from typing import List

def find_html_tags(html_content: str) -> List[str]:
    """
    Return a list of all HTML tags found in the input string.

    Parameters
    ----------
    html_content : str
        The HTML content to search for tags.

    Returns
    -------
    List[str]
        A list of strings, each string being a matched HTML tag.
    """
    # Use a non‑greedy pattern that does not allow nested '>' inside attributes
    tag_pattern = re.compile(r'<[^>]*?>', flags=re.IGNORECASE)

    try:
        return tag_pattern.findall(html_content)
    except Exception:  # pragma: no cover
        # In case of any unexpected error, return an empty list instead of raising.
        return []