import re
from typing import List

def extract_html_tags(html_content: str) -> List[str]:
    """
    Extract all HTML tags from the given string.

    The function uses a simple, non‑capturing regular expression
    that matches any sequence starting with '<', followed by one or more
    characters that are not '>', and ending with '>'. This pattern is
    deliberately simple to avoid the risk of catastrophic backtracking
    (CWE‑1333) and ensures linear time complexity in the length of the
    input string.

    Parameters:
        html_content (str): The HTML content to parse.

    Returns:
        List[str]: A list of tags found in the input string. If no tags
                   are present, an empty list is returned.
    """
    if not isinstance(html_content, str):
        # Gracefully handle non-string input by returning an empty list
        return []

    # Compile the regex once for efficiency.  The pattern is simple enough
    # that re.compile will not incur significant overhead.
    tag_pattern = re.compile(r'<[^>]+>')
    return tag_pattern.findall(html_content)