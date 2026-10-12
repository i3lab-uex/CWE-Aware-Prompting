import re
from typing import List

def extract_html_elements(document: str) -> List[str]:
    """
    Return a list of all substrings in *document* that match an HTML tag.
    Tags are identified by the pattern <...> where ... does not contain '>'.
    
    Parameters
    ----------
    document : str
        The input HTML content to analyze.
    
    Returns
    -------
    List[str]
        A list of matched tag strings in the order they appear.
    
    Notes
    -----
    - The function uses a non-greedy regex that stops at the first '>' after '<'.
    - It does not attempt to parse malformed HTML; it simply returns all
      substrings that look like tags.
    - No exceptions are raised even if *document* is empty or contains no tags.
    """
    # Compile the regex once for efficiency; it matches '<', then any
    # number of characters that are not '>', and finally a '>'.
    tag_pattern = re.compile(r'<[^>]+>')
    
    # Find all non-overlapping matches in the document
    return tag_pattern.findall(document)