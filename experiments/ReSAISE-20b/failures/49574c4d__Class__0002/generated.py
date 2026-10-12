import re
from typing import List

def extract_html_elements(document: str) -> List[str]:
    """
    Extracts all HTML tags from the given document string.

    Parameters
    ----------
    document : str
        The input HTML content to be analyzed.

    Returns
    -------
    List[str]
        A list of strings, each representing an HTML tag found in the input.
        The tags are returned in the order they appear in the document.

    Notes
    -----
    * The function uses a non-greedy regular expression to match tags,
      which mitigates the risk of catastrophic backtracking (CWE-407).
    * No exceptions are raised; invalid input simply results in an empty list.
    """
    if not isinstance(document, str):
        # Gracefully handle non-string inputs by returning an empty list.
        return []

    # Compile the pattern once for efficiency and to avoid repeated regex engine overhead.
    _tag_pattern = re.compile(r'<[^>]+?>', flags=re.IGNORECASE)

    # Find all non-overlapping matches in the document.
    return _tag_pattern.findall(document)