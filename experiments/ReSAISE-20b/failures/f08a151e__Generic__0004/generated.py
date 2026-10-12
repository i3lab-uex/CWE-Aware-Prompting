import re
from typing import List

def get_html_tags(html_input: str) -> List[str]:
    """
    Extracts all HTML tags from the provided string.

    Parameters
    ----------
    html_input : str
        The input HTML-formatted string.

    Returns
    -------
    List[str]
        A list of strings, each representing an HTML tag found in the input.
        The tags are returned exactly as they appear (including angle brackets
        and any attributes).

    Notes
    -----
    * The function uses a non-greedy regular expression to match tags.
    * It intentionally does not attempt to parse malformed HTML; it simply
      captures any substring that looks like a tag.
    * No exceptions are raised for normal operation; if the input is not
      a string, it will be coerced to ``str``.
    """
    if not isinstance(html_input, str):
        html_input = str(html_input)

    # Regex to match any tag: <tag ...>, </tag>, <tag/>, <!DOCTYPE ...>
    # It does not try to validate the tag structure.
    pattern = r'<[^>]+?>'
    return re.findall(pattern, html_input)