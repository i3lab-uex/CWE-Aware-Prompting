import re

def is_malicious_scheme(input_url: str) -> bool:
    """
    Determine if a string contains a potentially dangerous URL scheme.
    
    The function looks for the following schemes at the beginning of the string
    (ignoring leading whitespace):
    
      * javascript:
      * vbscript:
      * data:  (except when the media type is an image, e.g. data:image/png;...)
    
    Parameters
    ----------
    input_url : str
        The string to examine.
    
    Returns
    -------
    bool
        True if a malicious scheme is detected, False otherwise.
    
    Notes
    -----
    The regex is intentionally simple and case‑insensitive.  It does not attempt
    to fully parse URLs; it merely detects the dangerous scheme prefix.
    
    Raises
    ------
    re.error
        If the regular expression fails to compile (unlikely with a literal
        pattern).
    """
    if not isinstance(input_url, str):
        return False

    # Pattern matches:
    #   - leading whitespace
    #   - one of the dangerous schemes followed by a colon,
    #     or data: that is not followed by "image/"
    pattern = r'^\s*(?:(?:javascript|vbscript)[:]|data:(?!image/))'
    return re.search(pattern, input_url, flags=re.IGNORECASE) is not None