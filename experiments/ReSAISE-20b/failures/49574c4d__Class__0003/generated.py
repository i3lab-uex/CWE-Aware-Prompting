import re
from typing import List

def extract_html_elements(document: str) -> List[str]:
    """
    Return a list of all substrings that look like HTML tags in the given document.
    
    A tag is defined as a '<' followed by any characters that are not '>'
    and ending with a '>'. The pattern is non-greedy to avoid overmatching
    across multiple tags.
    
    Parameters:
        document (str): The input string containing HTML content.
        
    Returns:
        List[str]: A list of tag strings found in the document.  If no tags
                   are found, an empty list is returned.
    """
    # Non-greedy match of anything between < and > that does not contain >
    tag_pattern = re.compile(r'<[^>]+?>', flags=re.UNICODE)
    
    # Find all matches; returns an empty list if none found
    return tag_pattern.findall(document)