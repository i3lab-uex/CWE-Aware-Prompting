import re
from typing import List

# Compile the pattern once to avoid recompilation overhead.
_TAG_PATTERN = re.compile(r'<[^>]+>', flags=re.DOTALL)

def extract_html_tags(html_content: str) -> List[str]:
    """
    Extract all HTML tags from the provided string.

    Parameters
    ----------
    html_content : str
        The HTML content to parse.

    Returns
    -------
    List[str]
        A list of all tags found in the input string.  Tags are returned
        exactly as they appear, including angle brackets.

    Notes
    -----
    - The function uses a non‑greedy pattern that matches any sequence of
      characters that does not contain the closing angle bracket.
    - It is intentionally simple and avoids complex backtracking patterns
      that could lead to exponential runtime (CWE‑1333).
    - The function never raises an exception for normal input; if
      ``html_content`` is not a string, it will be coerced to one.
    """
    if not isinstance(html_content, str):
        html_content = str(html_content)

    # Find all substrings that look like tags.
    return _TAG_PATTERN.findall(html_content)