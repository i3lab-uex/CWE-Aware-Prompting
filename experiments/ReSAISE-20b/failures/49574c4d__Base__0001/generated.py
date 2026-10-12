import re

def extract_html_elements(document: str) -> list[str]:
    """
    Return a list of all HTML tags found in *document*.
    
    The function uses a non‑greedy regular expression that matches any
    substring starting with '<', followed by any number of characters except '>',
    and ending with a '>'. This pattern is simple enough to avoid
    catastrophic backtracking while still capturing typical HTML tags.
    
    Parameters:
        document (str): The input string containing potential HTML markup.
        
    Returns:
        list[str]: A list of matched tag strings. Empty if none found.
    
    Note:
        No exceptions are raised by this function; any unexpected input
        results in an empty list.
    """
    try:
        # Compile once for efficiency; use a non-greedy quantifier to avoid
        # excessive backtracking (CWE-1333 mitigation).
        tag_pattern = re.compile(r'<[^>]+?>')
        return tag_pattern.findall(document)
    except Exception:
        # In the unlikely event of an error, return an empty list
        return []