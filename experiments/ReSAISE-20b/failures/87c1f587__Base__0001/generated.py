import re

def find_html_tags(html_content: str):
    """
    Return a list of all substrings that look like HTML tags in the given string.

    Parameters
    ----------
    html_content : str
        The input HTML content to be scanned.

    Returns
    -------
    list[str]
        A list containing every matched tag in the order they appear.
    """
    # Compile a non‑greedy pattern that matches < ... > without backtracking
    tag_pattern = re.compile(r'<[^>]+>')
    return tag_pattern.findall(html_content)