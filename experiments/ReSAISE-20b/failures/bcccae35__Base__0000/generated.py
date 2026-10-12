import re

def parse_html_tags(html: str) -> list[str]:
    """
    Extract all HTML tags from the input string.

    Parameters
    ----------
    html : str
        The input HTML string to be parsed.

    Returns
    -------
    list[str]
        A list of strings, each representing an HTML tag found in the input.
        If no tags are found, returns an empty list.

    Notes
    -----
    * The regular expression is deliberately simple and efficient:
      it matches a '<' followed by any number of characters that are not '>'
      and then a closing '>'. This avoids the catastrophic backtracking
      issues associated with more complex patterns.
    * The function never raises an exception; any errors are silently
      handled by returning an empty list.
    """
    if not isinstance(html, str):
        # Non-string input is considered invalid; return empty list.
        return []

    # Compile the regex once for efficiency.  The pattern is simple and
    # does not contain backreferences or nested groups that could lead to
    # exponential time complexity (CWE-1333).
    tag_pattern = re.compile(r'<[^>]+>', flags=re.DOTALL)

    # Use findall to return all non-overlapping matches.
    tags = tag_pattern.findall(html)

    # Ensure the result is always a list (even if no matches are found).
    return tags