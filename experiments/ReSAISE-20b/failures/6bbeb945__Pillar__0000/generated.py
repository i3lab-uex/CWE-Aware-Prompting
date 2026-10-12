import re
from typing import Optional

# Regular expression to match potentially dangerous schemes.
# We ignore case and allow leading whitespace.
_DANGEROUS_SCHEMES = re.compile(r'^\s*(javascript|vbscript)', re.IGNORECASE)

def _is_safe_data_url(data: str) -> bool:
    """
    Determine whether a data URL is safe. A data URL is considered safe
    if its media type starts with 'image/'.
    
    Parameters
    ----------
    data : str
        The part of the URL after 'data:'.
    
    Returns
    -------
    bool
        True if the data URL is safe, False otherwise.
    """
    # Strip leading whitespace and split at the first ';' or ',' (separator).
    data = data.lstrip()
    # The media type is the part before ';' or ','.
    sep_match = re.search(r'[;,]', data)
    media_type = data[:sep_match.start()] if sep_match else data
    return media_type.lower().startswith('image/')

def has_dangerous_scheme(uri_str: str) -> bool:
    """
    Check whether the given string contains a potentially dangerous URL scheme.
    
    The function considers 'javascript:' and 'vbscript:' as inherently
    dangerous. For data URLs, the function allows image-based data URIs
    (e.g., 'data:image/png;base64,...') but flags others as dangerous.
    
    Parameters
    ----------
    uri_str : str
        The URI string to examine.
    
    Returns
    -------
    bool
        True if a dangerous scheme is detected, False otherwise.
    
    Raises
    ------
    re.error
        If the regular expression fails to compile or match.
    """
    if not isinstance(uri_str, str):
        raise TypeError("uri_str must be a string")

    # Check for javascript or vbscript schemes.
    if _DANGEROUS_SCHEMES.match(uri_str):
        return True

    # Check for data: scheme.
    uri_lower = uri_str.lstrip().lower()
    if uri_lower.startswith('data:'):
        # Extract the part after 'data:'.
        data_part = uri_str[5:]  # keep original case for media type check
        if not _is_safe_data_url(data_part):
            return True

    return False