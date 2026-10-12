import re

def get_html_tags(html_input: str) -> list[str]:
    """
    Extract all HTML tags from the given string.

    The function uses a non-greedy regular expression that matches
    any sequence of characters between '<' and '>' without
    including the closing angle bracket. This pattern is simple
    enough to avoid catastrophic backtracking (CWE-1333) while
    still correctly identifying tags in typical HTML input.

    Parameters:
        html_input (str): The string containing HTML markup.

    Returns:
        list[str]: A list of tag strings, e.g. ['<div>', '</p>'].
    """
    # The regex is intentionally simple and non-greedy:
    #   <          : match the opening '<'
    #   [^>]+      : one or more characters that are not '>'
    #   >          : match the closing '>'
    #
    # This pattern cannot exhibit exponential blow‑up because it
    # does not contain nested or overlapping quantifiers.
    tag_pattern = re.compile(r'<[^>]+>', flags=re.IGNORECASE)

    # `findall` returns a list of all non-overlapping matches.
    return tag_pattern.findall(html_input or "")