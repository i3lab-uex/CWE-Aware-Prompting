import re
from typing import List

def find_html_tags(html_string: str) -> List[str]:
    """
    Extracts all HTML tags from the given string.

    Parameters
    ----------
    html_string : str
        The input string containing HTML markup.

    Returns
    -------
    List[str]
        A list of tag strings (e.g., "<div>", "</p>", "<img src='...'>") found in the input.
        The list preserves the order of appearance.

    Notes
    -----
    - This function uses a non-greedy regular expression to match tags.
    - It does not parse or validate the HTML structure; it simply finds substrings that look like tags.
    - Self-closing tags, comments, and DOCTYPE declarations are also returned as separate entries.
    """
    if not isinstance(html_string, str):
        # In case a non-string is passed, return an empty list rather than raising.
        return []

    # Regular expression to match:
    #   * opening tags: <tag ...>
    #   * closing tags: </tag>
    #   * self-closing tags: <tag .../>
    #   * comments: <!-- comment -->
    #   * DOCTYPE declarations: <!DOCTYPE html>
    #
    # We capture the entire tag, including angle brackets.
    tag_pattern = re.compile(
        r'''
        <               # opening <
        \s*             # optional whitespace
        (?:!DOCTYPE\s+   # <!DOCTYPE ...>
          |!--           # <!-- comment
          |/?[a-zA-Z0-9]   # <tag or </tag (first char of tag name)
        )
        [^>]*?          # any characters except >, non-greedy
        >               # closing >
        ''',
        re.IGNORECASE | re.VERBOSE,
    )

    tags = tag_pattern.findall(html_string)
    return tags