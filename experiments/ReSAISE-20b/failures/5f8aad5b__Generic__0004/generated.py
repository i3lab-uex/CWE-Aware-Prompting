import re
from typing import List

def extract_html_tags(html_content: str) -> List[str]:
    """
    Extracts all HTML tag names from the given string.

    Parameters
    ----------
    html_content : str
        The HTML content to parse.

    Returns
    -------
    List[str]
        A list of tag names found in the input string. The order
        corresponds to their first appearance.

    Notes
    -----
    * Self‑closing tags and void elements are treated the same as normal tags.
    * The function ignores content inside comments, CDATA sections,
      or scripts/styles. It simply looks for patterns that start with
      '<' followed by a tag name.
    * No exceptions are raised for malformed input; the function
      gracefully returns an empty list if no tags are found.
    """
    # Regex to capture tag names:
    #   <\s*         : opening '<' optionally followed by whitespace
    #   ([a-zA-Z0-9]+) : capture group for the tag name (letters or digits)
    #   [^>]*?>      : any characters except '>' until the first '>'
    tag_pattern = re.compile(r'<\s*([a-zA-Z0-9]+)[^>]*?>', re.IGNORECASE)

    # Find all matches; each match is a tuple where the first element is the tag name
    tags = [match[0] for match in re.findall(tag_pattern, html_content)]
    return tags