import re
from typing import List

# Compile the regex once to avoid repeated compilation overhead.
# The pattern matches an opening '<', followed by any number of
# characters that are not '>' (non-greedy), and ends with a closing '>'.
_TAG_RE = re.compile(r'<[^>]+>', re.DOTALL)

def extract_html_tags(html_content: str) -> List[str]:
    """
    Extract all HTML tags from the given string.

    Parameters
    ----------
    html_content : str
        The input HTML content as a string.

    Returns
    -------
    List[str]
        A list of tag strings, including the surrounding angle brackets.
        The order is the same as they appear in the input string.

    Notes
    -----
    * The function never raises an exception on normal operation.
      Any unexpected input (e.g., ``None``) is treated as an empty string.
    * The regex is deliberately simple to avoid catastrophic backtracking
      and keeps the worst‑case time complexity linear in the size of the input.
    """
    if not isinstance(html_content, str):
        # Gracefully handle non‑string input by treating it as empty.
        return []

    # Find all matches and convert the iterator to a list.
    return _TAG_RE.findall(html_content)