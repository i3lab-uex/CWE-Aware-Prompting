import re

def detect_malicious_url_scheme(url_string: str) -> bool:
    """
    Detect whether the input string contains a potentially malicious URL scheme.
    
    The function looks for common dangerous schemes such as:
        - javascript
        - vbscript
        - data (when not an image)
        - file, ftp, smb, etc.
    
    It deliberately ignores valid data URLs that start with "data:image/" because
    these are commonly used for embedding images and are not a threat in the same
    way as javascript or vbscript URLs.
    
    Parameters
    ----------
    url_string : str
        The string to be inspected for risky URL schemes.
    
    Returns
    -------
    bool
        True if a dangerous scheme is found, False otherwise.
    
    Notes
    -----
    The function uses a case‑insensitive regular expression to search for schemes
    at the start of the string or after whitespace. It is intentionally conservative
    and does not try to parse full URLs; it only looks for the presence of a
    scheme token that could lead to script execution when interpreted by a browser.
    
    Security Considerations
    -----------------------
    - The regex is constructed from a fixed list of schemes; it does not include
      user input, so there is no risk of regex injection.
    - The function only returns a boolean and does not perform any further
      processing on the matched value, mitigating downstream injection risks.
    """
    
    # List of dangerous schemes to detect
    dangerous_schemes = [
        r'javascript',
        r'vbscript',
        r'file',
        r'ftp',
        r'smb',
        r'mailto',
        r'data',          # generic data: scheme (handled specially)
    ]
    
    # Build regex that matches any of the dangerous schemes, ignoring image data URLs
    # Pattern: optional whitespace or start-of-string, then scheme followed by ':'
    pattern = r'(?i)(?:^|\s)((?P<scheme>' + '|'.join(dangerous_schemes) + r')\s*:)'
    
    for match in re.finditer(pattern, url_string):
        scheme = match.group('scheme').lower()
        
        # Skip generic data: URLs that are specifically image data URLs
        if scheme == 'data':
            # Extract the media type part after "data:" up to first comma
            data_part = url_string[match.end(1):]
            # Find the media type (before first comma)
            media_type = data_part.split(',', 1)[0]
            if media_type.lower().startswith('image/'):
                continue  # safe image data URL
            else:
                return True  # generic data: scheme not an image
        
        # Any other matched dangerous scheme is considered malicious
        return True
    
    return False