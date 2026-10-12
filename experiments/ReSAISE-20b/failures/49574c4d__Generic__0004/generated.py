import re
from typing import List

# Regular expression to match simple HTML tags.
# It captures anything that starts with '<', followed by any characters except '>'
# until the next '>'. This includes opening, closing and self‑closing tags.
_TAG_RE = re.compile(r'<[^>]+>', flags=re.IGNORECASE | re.DOTALL)

def extract_html_elements(document: str) -> List[str]:
    """
    Extract all HTML tags from the provided document string.

    Parameters
    ----------
    document : str
        The input HTML content to be analyzed.

    Returns
    -------
    List[str]
        A list of strings, each string being a matched HTML tag.
        If no tags are found an empty list is returned.

    Notes
    -----
    - The function uses a simple regular expression that matches any sequence
      starting with '<' and ending at the next '>'. It does not attempt to parse
      nested tags or validate HTML structure.
    - No exceptions are raised; if the input is not a string, it will be
      converted to ``str`` implicitly by Python's ``re`` module.
    """
    if not isinstance(document, str):
        document = str(document)

    return _TAG_RE.findall(document)