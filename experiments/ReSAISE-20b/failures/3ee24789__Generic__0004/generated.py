import re

def detect_html_tags(html_str: str) -> list[str]:
    """
    Detect all HTML tags in the given string.

    Parameters
    ----------
    html_str : str
        The input HTML content to be analyzed.

    Returns
    -------
    list[str]
        A list of strings, each representing an HTML tag found in the input.
        The tags are returned exactly as they appear (including angle brackets).

    Notes
    -----
    * The function uses a simple regular expression that matches any substring
      starting with '<', followed by any characters except '>' (non-greedy),
      and ending with '>'. This captures start tags, end tags, self-closing
      tags, and comments.
    * No exceptions are raised; if the input is not a string or is empty,
      an empty list is returned.
    """
    if not isinstance(html_str, str):
        return []

    # Regular expression to match HTML tags.
    # Non-greedy to avoid spanning multiple tags if a stray '>' appears inside an attribute.
    tag_pattern = re.compile(r"<[^>]+?>", re.DOTALL)

    return tag_pattern.findall(html_str)