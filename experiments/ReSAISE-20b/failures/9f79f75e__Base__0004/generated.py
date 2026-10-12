import re
from typing import List

# Compile the regex once at module load time to avoid repeated compilation.
_TAG_RE = re.compile(r'</?[a-zA-Z][^>]*>', re.IGNORECASE)

def find_html_tags(html_string: str) -> List[str]:
    """
    Extract all HTML tags from the provided string.

    Parameters
    ----------
    html_string : str
        The input string containing HTML markup.

    Returns
    -------
    List[str]
        A list of all tags found in the input string, preserving order.
    """
    # The regex is simple and non-greedy; it matches opening, closing,
    # self-closing tags, and any attributes without consuming '>'.
    return _TAG_RE.findall(html_string)