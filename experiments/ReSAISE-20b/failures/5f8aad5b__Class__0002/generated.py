import re
from typing import List

def extract_html_tags(html_content: str) -> List[str]:
    """
    Extract all HTML tags from the provided string.

    Parameters
    ----------
    html_content : str
        A string containing HTML markup.

    Returns
    -------
    List[str]
        A list of tags (including the surrounding angle brackets) that appear in
        ``html_content``.  The order of tags is preserved as they occur in the
        input string.

    Notes
    -----
    * The function is intentionally conservative: it matches any opening or
      closing tag that starts with '<' and ends at the first '>' encountered.
    * The regular expression is written to avoid catastrophic backtracking
      (CWE‑407) by using a non‑greedy quantifier and restricting the character
      set inside the tag.
    * The function never raises an exception for normal input; if a regex
      compilation error occurs it returns an empty list.
    """
    # Regular expression to match simple HTML tags.
    #   - '<' followed by optional '/' for closing tags,
    #   - then a tag name consisting of word characters or hyphens,
    #   - followed by optional attributes (anything that is not '>'),
    #   - finally the closing '>'.
    tag_pattern = r'<\s*\/?\s*\w[\w:-]*[^>]*?>'

    try:
        regex = re.compile(tag_pattern, flags=re.IGNORECASE | re.DOTALL)
    except re.error:
        # If the regex cannot be compiled, return an empty list.
        return []

    # Find all non-overlapping matches in the string.
    tags = regex.findall(html_content)

    return tags