import re
from typing import List

# Pre‑compile a safe, non‑greedy regex for tag extraction.
_TAG_RE = re.compile(r'<[^>]+?>', flags=re.IGNORECASE | re.UNICODE)

def extract_html_tags(html_content: str) -> List[str]:
    """
    Extract all HTML tags from the given string.

    The function returns a list of tag strings, including their surrounding
    angle brackets and any attributes. It is tolerant to malformed input
    and will never raise an exception for normal usage.

    Parameters
    ----------
    html_content : str
        The HTML content to parse.

    Returns
    -------
    List[str]
        A list of all tags found in the input string. If no tags are present,
        an empty list is returned.
    """
    try:
        # Using the pre‑compiled regex ensures efficient matching
        return _TAG_RE.findall(html_content)
    except Exception:
        # In the unlikely event of a regex failure, return an empty list
        return []