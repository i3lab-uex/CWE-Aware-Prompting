import re
from typing import List

def extract_html_elements(document: str) -> List[str]:
    """
    Extract all HTML tags from the given document string.

    Parameters
    ----------
    document : str
        The input HTML content to analyze.

    Returns
    -------
    List[str]
        A list of all substrings that match HTML tag patterns.
        Each element is a complete tag, including its angle brackets
        and any attributes or closing slashes.

    Notes
    -----
    - The function is intentionally simple and uses a non-greedy
      regular expression to match tags. It does not attempt to validate
      HTML structure or handle malformed markup.
    - No exceptions are raised; if the input is not a string, it will
      be coerced to ``str`` and processed safely.
    """
    # Ensure the input is a string; non-string inputs are coerced
    if not isinstance(document, str):
        document = str(document)

    # Regex to match any sequence that starts with '<', ends with '>',
    # and does not contain a '>' inside (non-greedy).
    tag_pattern = re.compile(r'<[^>]+?>')

    # Find all matches and return them as a list
    return tag_pattern.findall(document)