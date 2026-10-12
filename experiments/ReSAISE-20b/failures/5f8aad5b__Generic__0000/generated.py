import re
from typing import List

def extract_html_tags(html_content: str) -> List[str]:
    """
    Extract all HTML tags from the given string.

    Parameters
    ----------
    html_content : str
        The input HTML content as a string.

    Returns
    -------
    List[str]
        A list of all tags found in the input string.  Tags are returned
        exactly as they appear, including the angle brackets and any
        attributes.  Comments (<!-- ... -->) are ignored.

    Notes
    -----
    - The function is tolerant to malformed HTML; it simply finds the
      next '>' character after a '<'.
    - It does not attempt to parse nested tags or handle self‑closing
      syntax beyond the basic regex.
    - No exceptions are raised under normal usage.  If ``html_content``
      is not a string, it will be coerced to one via ``str()``.
    """
    if not isinstance(html_content, str):
        html_content = str(html_content)

    # Regular expression to match tags while ignoring comments.
    tag_pattern = re.compile(
        r"""
        <
        (?:
            ![ \t]*--.*?--      # comments, e.g. <!-- comment -->
          | [^\s>]+             # tag name
        )
        (?:[^<>]*?)              # attributes or whitespace
        >
        """,
        re.DOTALL | re.VERBOSE,
    )

    # Find all matches; filter out comment tags.
    raw_matches = tag_pattern.findall(html_content)

    # The pattern captures the entire tag; comments are excluded by
    # the negative lookahead, but to be safe we filter them out.
    tags = [
        match
        for match in raw_matches
        if not re.match(r"<!--.*-->", match, re.DOTALL)
    ]

    return tags