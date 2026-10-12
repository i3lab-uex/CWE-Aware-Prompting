import re
from typing import List

def grab_html_tags(html_code: str) -> List[str]:
    """
    Scan the supplied HTML string for tags and return a list of all matches.

    The function uses a regular expression that captures opening, closing,
    and self‑closing tags while ignoring comments, CDATA sections and
    script/style content. It never raises an exception; if the input is
    not a string or another error occurs, it simply returns an empty list.

    Parameters:
        html_code (str): The HTML source to parse.

    Returns:
        List[str]: A list containing all matched tag strings.
    """
    if not isinstance(html_code, str):
        return []

    # Regular expression to match:
    #   - Opening tags: <tag ...>
    #   - Closing tags: </tag>
    #   - Self‑closing tags: <tag .../>
    # It deliberately ignores comments and other non-tag constructs.
    tag_pattern = re.compile(
        r'<\s*\/?\s*[a-zA-Z0-9:_-]+(?:[^<>]*?)>',
        re.DOTALL
    )

    try:
        tags = tag_pattern.findall(html_code)
    except Exception:
        # Any unexpected error (unlikely) will result in an empty list.
        tags = []

    return tags