import re

def detect_html_tags(html_str: str) -> list[str]:
    """
    Return a list of all HTML tags found in the input string.
    
    The function uses a simple, non-backtracking regular expression that
    matches an opening angle bracket, optional whitespace, any number of
    characters that are not a closing bracket, and finally a closing
    angle bracket.  The pattern is deliberately non-greedy to avoid
    catastrophic backtracking (CWE‑1333) and is safe for typical HTML.
    
    Parameters
    ----------
    html_str : str
        The input string containing potential HTML markup.
    
    Returns
    -------
    list[str]
        A list of matched tags, including the surrounding angle brackets.
    
    Notes
    -----
    - The function does not attempt to validate the tags; it merely extracts
      substrings that look like HTML tags.
    - No exceptions are raised; if the input is not a string, it will be
      converted to one via ``str()``.
    """
    if not isinstance(html_str, str):
        html_str = str(html_str)

    # Pattern: < ... >  where '...' does not contain a '>' character.
    tag_pattern = re.compile(r"<\s*[^>]+?>")
    return tag_pattern.findall(html_str)