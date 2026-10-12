import re
from typing import List

def extract_html_tags(html_string: str) -> List[str]:
    """
    Extracts all HTML tags from the given string.

    Parameters
    ----------
    html_string : str
        The input HTML content to parse.

    Returns
    -------
    List[str]
        A list of all tags found, including the surrounding angle brackets.
        The order matches their appearance in the input string.

    Notes
    -----
    * The function is intentionally simple and uses a regular expression.
      It does not attempt to parse nested or malformed tags correctly,
      but it reliably captures well‑formed opening and closing tags.
    * No exceptions are raised; invalid input simply results in an empty list.
    """
    if not isinstance(html_string, str):
        # Defensive: treat non‑string input as empty content.
        return []

    # Regex pattern:
    #   <\s*[^>]+?>  : match a '<', optional whitespace, then
    #   any characters except '>' lazily until the first '>'.
    # This captures tags like <div>, </a>, <img src="...">, etc.
    tag_pattern = re.compile(r'<\s*[^>]+?>', flags=re.IGNORECASE)

    # Find all non‑overlapping matches
    tags = tag_pattern.findall(html_string)
    return tags if tags is not None else []