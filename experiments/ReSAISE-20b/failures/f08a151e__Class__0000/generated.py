import re
from typing import List

# Regular expression to match HTML tags.
# It captures:
#   - an opening '<'
#   - optional whitespace
#   - an optional '/' for closing tags
#   - a tag name consisting of word characters (letters, digits, underscore)
#   - any characters that are not '>' (attributes, etc.), captured non-greedily
#   - the closing '>'
_TAG_RE = re.compile(r'<\s*/?\s*\w+[^>]*?>', flags=re.IGNORECASE)


def get_html_tags(html_input: str) -> List[str]:
    """
    Extracts all HTML tags from the given input string.

    The function is intentionally simple and efficient.  It uses a
    precompiled regular expression that matches tags without backtracking
    over the entire input.  The pattern is deliberately non-greedy and
    does not contain nested quantifiers that could trigger catastrophic
    backtracking (CWE-407).

    Parameters
    ----------
    html_input : str
        A string containing HTML markup.

    Returns
    -------
    List[str]
        A list of all tags found in the input.  The order is preserved
        as they appear in the string.

    Raises
    ------
    None
        The function is designed to never raise exceptions for normal
        input.  If `html_input` is not a string, it will be converted to
        one using ``str()``.
    """
    if not isinstance(html_input, str):
        html_input = str(html_input)

    # Find all matches; re.findall returns a list of strings.
    return _TAG_RE.findall(html_input)