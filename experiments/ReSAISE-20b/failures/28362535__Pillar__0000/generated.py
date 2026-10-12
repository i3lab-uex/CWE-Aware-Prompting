import re

# Regular expression that matches a dangerous URL scheme at the beginning of a string.
#   - It allows optional leading whitespace and comment characters (`/* ... */`).
#   - It matches `javascript:` or `vbscript:` schemes, case‑insensitively.
#   - It also allows URLs that start with `data:` but only if the media type is NOT an image.
#     Any other data URLs are considered dangerous.
DANGEROUS_SCHEME_RE = re.compile(
    r"""
    ^\s*                                 # Optional leading whitespace
    (?:                                   # Start non‑capturing group for scheme checks
        (?:
            javascript:                  # `javascript:` scheme
          | vbscript:                    # `vbscript:` scheme
        )
      |
        data:
        (?!\s*image\/)                   # Not an image MIME type
    )
    """,
    re.IGNORECASE | re.VERBOSE,
)

def is_malicious_scheme(input_url: str) -> bool:
    """
    Return True if the supplied string contains a potentially dangerous URL scheme.
    
    The function treats `javascript:` and `vbscript:` schemes as unsafe. 
    It also flags any `data:` URL that is not an image MIME type (e.g. 
    `data:text/html;...`). Image data URLs (`data:image/...`) are considered safe.
    
    Parameters
    ----------
    input_url : str
        The URL string to examine.
    
    Returns
    -------
    bool
        True if a malicious scheme is detected, False otherwise.
    
    Raises
    ------
    re.error
        If the regular expression fails to compile (unlikely since it is pre‑compiled).
    """
    if not isinstance(input_url, str):
        # Non‑string inputs are considered unsafe by default.
        return True

    # Strip leading/trailing whitespace for a cleaner match
    trimmed = input_url.strip()

    # Use the compiled regex to detect dangerous schemes.
    return bool(DANGEROUS_SCHEME_RE.match(trimmed))