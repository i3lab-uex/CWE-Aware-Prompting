import re
from typing import List

def extract_html_tags(html_content: str) -> List[str]:
    """
    Extracts HTML tags from the given string using a non‑greedy regular expression.
    
    Parameters
    ----------
    html_content : str
        A string containing HTML markup.

    Returns
    -------
    List[str]
        A list of tag names (including any attributes) found in the input.
    
    Notes
    -----
    The function uses a simple, non‑backtracking pattern that matches anything between
    '<' and '>' characters. This mitigates the risk of catastrophic backtracking (CWE‑1333).
    """
    if not isinstance(html_content, str):
        return []

    # Non‑greedy match for anything between < and >, ensuring minimal consumption
    tag_pattern = re.compile(r"<[^>]+>", re.DOTALL)

    # Find all matches; each match is a complete tag string
    tags = tag_pattern.findall(html_content)

    return tags