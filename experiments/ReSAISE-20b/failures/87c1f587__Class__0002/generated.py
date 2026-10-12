import re
from typing import List

def find_html_tags(html_content: str) -> List[str]:
    """
    Return a list of all substrings that look like HTML tags in the input string.
    
    A tag is defined as a '<' character followed by any number of characters that are
    not '>' and terminated by the first '>' encountered. This simple pattern is
    intentionally non‑capturing of nested tags or malformed input to keep the
    algorithm linear in time and avoid catastrophic backtracking.
    
    Parameters
    ----------
    html_content : str
        The HTML source to search for tags.
    
    Returns
    -------
    List[str]
        A list of tag strings, including the surrounding angle brackets.
    
    Notes
    -----
    - The function is defensive: it never raises an exception even if the input is
      not a string. Non‑string arguments are coerced to ``str``.
    - The regex pattern uses a negated character class `[^>]*` to consume all
      characters until the first '>' is found, which guarantees O(n) complexity.
    """
    if not isinstance(html_content, str):
        html_content = str(html_content)

    # Pattern: '<' followed by any number of non-'>' characters, then '>'
    tag_pattern = re.compile(r'<[^>]*>', flags=re.IGNORECASE)

    # Find all non-overlapping matches
    return tag_pattern.findall(html_content)