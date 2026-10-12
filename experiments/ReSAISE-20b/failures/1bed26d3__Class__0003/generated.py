import re

def check_javascript_scheme(url_str: str) -> bool:
    """
    Determine whether the supplied string contains a potentially dangerous URL scheme.
    
    The function considers the following schemes as dangerous:
        - javascript
        - vbscript
    
    Image data URLs of the form `data:image/<type>;base64,...` are explicitly
    excluded from being flagged as dangerous.
    
    Parameters
    ----------
    url_str : str
        The string to be examined for a harmful URL scheme.
    
    Returns
    -------
    bool
        ``True`` if the string contains a dangerous scheme (excluding safe image data URLs),
        otherwise ``False``.
    
    Notes
    -----
    - The check is performed in a case‑insensitive manner.
    - Leading and trailing whitespace around the scheme are ignored.
    - The function is tolerant of malformed URLs; it simply returns ``False`` if no
      dangerous scheme is found.
    """
    
    # Normalise whitespace and case for reliable matching
    cleaned = url_str.strip().lower()
    
    # If it is a data URL for an image, we consider it safe
    if cleaned.startswith("data:image/"):
        return False
    
    # Dangerous schemes we want to detect
    dangerous_patterns = [
        r"^javascript\s*:",   # e.g. "javascript:" or "javascript :"
        r"^vbscript\s*:",     # e.g. "vbscript:"
    ]
    
    for pattern in dangerous_patterns:
        if re.match(pattern, cleaned):
            return True
    
    return False