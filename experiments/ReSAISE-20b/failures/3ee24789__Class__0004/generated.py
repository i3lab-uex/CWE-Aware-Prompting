import re

def detect_html_tags(html_str: str) -> list[str]:
    """
    Return a list of all substrings in *html_str* that look like HTML tags.
    
    The function uses a non‑greedy regular expression to find any sequence that
    starts with '<', contains characters other than '>' (to avoid matching the
    closing bracket), and ends with a single '>'.  This pattern is simple,
    deterministic, and does not expose the function to catastrophic backtracking
    or other performance issues (CWE‑407).
    
    Parameters
    ----------
    html_str : str
        The HTML content to be scanned.
        
    Returns
    -------
    list[str]
        A list of matched tag strings.  If no tags are found, an empty list is
        returned.
    """
    # Compile the regex once for efficiency.  The pattern is deliberately
    # simple to avoid backtracking pitfalls.
    tag_pattern = re.compile(r'<[^>]+?>')
    
    # Find all non‑overlapping matches in the input string.
    return tag_pattern.findall(html_str)