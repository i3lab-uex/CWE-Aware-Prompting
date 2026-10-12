import re

# Regular expression that captures the scheme part of a URL (everything before the first ':')
SCHEME_RE = re.compile(r'^\s*([a-zA-Z][a-zA-Z0-9+\-.]*):', re.IGNORECASE)

# List of known dangerous schemes that are generally considered unsafe
DANGEROUS_SCHEMES = {
    'javascript',
    'vbscript',
    'file',
    'data',          # data: is dangerous unless it contains a safe image MIME type
    'mailto',        # can be abused for phishing
    'ftp',           # potential for remote file access
    'gopher',
    'telnet',
}

# Regular expression that matches a safe image data URL
SAFE_IMAGE_DATA_RE = re.compile(
    r'^\s*data\s*:\s*(image/(?:png|jpeg|jpg|gif|bmp|webp))\s*;',
    re.IGNORECASE
)

def is_malicious_scheme(input_url: str) -> bool:
    """
    Detect if a string contains a potentially malicious URL scheme.
    
    Parameters
    ----------
    input_url : str
        The string to examine. It may contain a full URL or just the scheme.
    
    Returns
    -------
    bool
        True if a dangerous scheme is detected (excluding safe image data URLs),
        False otherwise.
    """
    # Strip leading/trailing whitespace to avoid false negatives
    url = input_url.strip()

    # Skip if the URL is a safe image data URI
    if SAFE_IMAGE_DATA_RE.match(url):
        return False

    # Extract the scheme (if any)
    match = SCHEME_RE.match(url)
    if not match:
        return False  # No scheme present

    scheme = match.group(1).lower()

    if scheme in DANGEROUS_SCHEMES:
        # Special handling for data: URLs
        if scheme == 'data':
            # If the data URL does not start with a safe image MIME type,
            # treat it as dangerous.
            return True
        return True

    return False