import re

def detect_malicious_url_scheme(url_string: str) -> bool:
    """
    Detects whether a URL string contains a potentially malicious scheme.
    
    The function considers the following schemes as dangerous:
        - javascript
        - vbscript
    
    It explicitly ignores valid image data URLs (e.g., `data:image/png;base64,...`).
    Any other `data:` scheme that is not an image is treated as suspicious.
    
    Parameters
    ----------
    url_string : str
        The URL string to inspect.

    Returns
    -------
    bool
        ``True`` if a dangerous scheme is detected, otherwise ``False``.

    Notes
    -----
    - The check is case‑insensitive and ignores leading whitespace.
    - The function is deliberately conservative: it flags any unknown
      `data:` scheme as suspicious, which helps mitigate the risk of
      obscure or future malicious schemes.
    """
    if not isinstance(url_string, str):
        return False

    # Strip leading whitespace and convert to lowercase for comparison
    trimmed = url_string.lstrip()
    lower = trimmed.lower()

    # 1. Directly malicious schemes
    if lower.startswith("javascript:") or lower.startswith("vbscript:"):
        return True

    # 2. data URLs – only allow image/* schemes
    if lower.startswith("data:"):
        # Allow only data:image/...;base64,... or data:image/... (no base64)
        if re.match(r"^data\s*:\s*image\/[^;]+(?:;base64,|$)", lower):
            return False
        # Any other data: scheme is suspicious
        return True

    # 3. No known malicious scheme detected
    return False