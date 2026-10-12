import re
from typing import List

def extract_html_tags(html_string: str) -> List[str]:
    """
    Extract all HTML tags from the provided string using a simple,
    non-greedy regular expression. The function is designed to avoid
    catastrophic backtracking and thus mitigates CWE-1333 concerns.

    Parameters:
        html_string (str): The input HTML content.

    Returns:
        List[str]: A list of matched tag strings, including the surrounding
                   angle brackets. If no tags are found an empty list is returned.
    """
    if not isinstance(html_string, str):
        # Gracefully handle non-string input by returning an empty list
        return []

    try:
        # Use a simple, non-greedy pattern that matches anything between
        # '<' and the next '>' without capturing nested tags.
        tag_pattern = re.compile(r'<[^>]+>', flags=re.DOTALL)
        return tag_pattern.findall(html_string)
    except re.error:
        # In the unlikely event that compilation fails, return an empty list
        return []