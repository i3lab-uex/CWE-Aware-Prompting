import re
from typing import List

def extract_html_tags(html_string: str) -> List[str]:
    """
    Extracts all HTML tags from the given string.

    Parameters
    ----------
    html_string : str
        The input string containing HTML markup.

    Returns
    -------
    List[str]
        A list of all tags found in the input. The order corresponds to their
        appearance in the string.

    Notes
    -----
    * The function is tolerant of malformed input and will never raise an exception.
    * It uses a non‑greedy regular expression to avoid capturing across multiple tags.
    * Comments, doctypes and processing instructions are treated as tags for simplicity.
    """
    if not isinstance(html_string, str):
        # If input is not a string, return an empty list safely.
        return []

    # Regular expression to match any sequence that starts with '<' and ends with '>'
    # The pattern uses a non-greedy quantifier to avoid spanning multiple tags.
    tag_pattern = re.compile(r'<[^>]*?>', re.DOTALL)

    try:
        tags = tag_pattern.findall(html_string)
    except Exception:  # pragma: no cover
        # In the unlikely event that regex processing fails, return empty list.
        tags = []

    return tags