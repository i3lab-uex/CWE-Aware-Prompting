import re
from typing import List

def extract_html_tags(html_string: str) -> List[str]:
    """
    Extracts all HTML tags from the provided string using a regular expression.

    Parameters
    ----------
    html_string : str
        The input HTML string to parse.

    Returns
    -------
    List[str]
        A list of all detected HTML tags, including angle brackets and any
        attributes or content within them. If no tags are found an empty list
        is returned.

    Notes
    -----
    - The function does not raise exceptions; any error during regex
      compilation or matching results in an empty list being returned.
    - The regular expression is intentionally simple: it matches the
      shortest sequence that starts with '<' and ends with '>' without
      interpreting nested tags or quoted angle brackets. This is adequate for
      basic tag extraction but not suitable for fully compliant HTML parsing.
    """
    # Use a non-greedy pattern to capture tags without overmatching.
    tag_pattern = r'<[^>]+>'
    try:
        # Compile the pattern once for efficiency.
        compiled = re.compile(tag_pattern, flags=re.IGNORECASE | re.DOTALL)
        matches = compiled.findall(html_string)
        return matches
    except Exception:
        # In case of any unexpected error, return an empty list safely.
        return []