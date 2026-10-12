import re
from typing import List

def find_html_tags(html_string: str) -> List[str]:
    """
    Extract all HTML tags from the provided string using a safe, non‑greedy regular expression.

    Parameters
    ----------
    html_string : str
        The input string containing HTML markup.

    Returns
    -------
    List[str]
        A list of tag strings (e.g., "<div>", "</p>", "<img src='...'>") found in the input.
    """
    # Non‑greedy match of any characters between '<' and '>' (excluding newlines for safety).
    # This pattern avoids catastrophic backtracking and is efficient even on large inputs.
    tag_pattern = re.compile(r'<[^>]+?>', flags=re.DOTALL)
    return tag_pattern.findall(html_string)