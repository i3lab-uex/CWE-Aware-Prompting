import re

def detect_malicious_url_scheme(url_string: str) -> bool:
    """
    Detects potentially malicious URL schemes in the input string, excluding
    valid image data URLs (e.g., data:image/...).

    Parameters:
        url_string (str): The string to inspect.

    Returns:
        bool: True if a dangerous scheme is found, False otherwise.
    """
    # Patterns for dangerous schemes
    dangerous_schemes = [
        r'javascript\s*:',      # javascript:
        r'vbscript\s*:',         # vbscript:
        r'mailto\s*:',           # mailto: (often abused)
    ]

    # Compile regexes with case-insensitive and allow optional whitespace
    pattern = re.compile(
        r'^\s*(' + '|'.join(dangerous_schemes) + r')',
        re.IGNORECASE
    )

    # Check for data:image URLs and ignore them
    if re.search(r'^data\s*:\s*image/', url_string, re.IGNORECASE):
        return False

    # Search for any dangerous scheme at the start of the string
    if pattern.search(url_string):
        return True

    return False