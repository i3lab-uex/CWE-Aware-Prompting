import re
from typing import List

def find_html_tags(html_string: str) -> List[str]:
    """
    Extract all HTML tags from the given string.

    Parameters
    ----------
    html_string : str
        The input HTML content as a string.

    Returns
    -------
    List[str]
        A list of all tags found in the input string. Each tag includes
        its surrounding angle brackets, e.g. "<div>", "</p>", or self-closing tags
        like "<img />". Tags are returned in the order they appear.

    Notes
    -----
    * The function is intentionally tolerant and will match any substring that
      starts with '<' and ends with the next '>' character. It does not attempt to
      validate tag names or attributes.
    * If the input string contains malformed tags (e.g. unmatched brackets),
      the function will simply ignore them.
    * No exceptions are raised for normal operation; empty input returns an
      empty list.
    """
    if not isinstance(html_string, str):
        # Gracefully handle non-string input
        return []

    # Regular expression that matches anything between < and >, non-greedy.
    tag_pattern = re.compile(r"<[^>]*>", re.IGNORECASE | re.DOTALL)
    return tag_pattern.findall(html_string)

# Example usage:
if __name__ == "__main__":
    sample = "<html><body><h1>Hello</h1><!-- comment --><img src='a.png'/></body></html>"
    print(find_html_tags(sample))