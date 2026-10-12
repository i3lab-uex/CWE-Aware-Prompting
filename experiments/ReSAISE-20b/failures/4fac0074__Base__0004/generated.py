import re
from typing import List

def extract_html_tags(html_string: str) -> List[str]:
    """
    Extract all HTML tags from the given string.

    Parameters
    ----------
    html_string : str
        The input string containing HTML content.

    Returns
    -------
    List[str]
        A list of all tags found in the input. If no tags are present,
        an empty list is returned.

    Notes
    -----
    * The function uses a non‑greedy pattern ``<[^>]+>`` which
      matches any sequence that starts with '<', contains one or more
      characters other than '>', and ends with '>'. This avoids the
      catastrophic backtracking issues that can arise with more complex
      patterns, keeping the runtime linear in the size of the input.
    * The function is defensive: if ``html_string`` is not a string
      (e.g., ``None``), it returns an empty list instead of raising.
    """
    if not isinstance(html_string, str):
        return []

    # Non‑greedy match for any tag; this pattern is safe from
    # exponential blowup and works in linear time.
    tag_pattern = re.compile(r'<[^>]+>')
    return tag_pattern.findall(html_string)