import re

# List of potentially dangerous URL schemes.
_DANGEROUS_SCHEMES = [
    r'javascript',
    r'vbscript',
    r'mailto',          # optional: consider it risky in some contexts
    r'file',
    r'ftp',
    r'ftps',
    r'ssh',
]

# Compile a regex that matches any of the dangerous schemes
# occurring at the start of a string or after whitespace, followed by ':'
_DANGEROUS_REGEX = re.compile(
    r'(?i)(?:^|\s)(' + '|'.join(_DANGEROUS_SCHEMES) + r')\s*:',
    flags=re.IGNORECASE
)

# Regex to detect a data URL that starts with 'data:' and is an image type.
_IMAGE_DATA_URL_REGEX = re.compile(
    r'(?i)^\s*data\s*:\s*image\/[^;]+',
    flags=re.IGNORECASE
)


def contains_dangerous_scheme(user_input: str) -> bool:
    """
    Return True if *user_input* contains a risky URL scheme such as
    javascript:, vbscript:, file:, etc., excluding valid image data URLs.
    
    Parameters:
        user_input (str): The string to inspect.
        
    Returns:
        bool: True if a dangerous scheme is found, False otherwise.
    """
    # Quick check for data:image URLs – they are safe.
    if _IMAGE_DATA_URL_REGEX.search(user_input):
        return False

    # Search for any dangerous scheme.
    if _DANGEROUS_REGEX.search(user_input):
        return True

    # No dangerous patterns found.
    return False