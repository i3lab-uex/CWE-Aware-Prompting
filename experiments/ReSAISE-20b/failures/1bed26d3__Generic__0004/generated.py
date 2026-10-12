import re

def check_javascript_scheme(url_str: str) -> bool:
    """
    Detects potentially dangerous URL schemes in a string, excluding safe image-based data URLs.

    Parameters
    ----------
    url_str : str
        The string to inspect for dangerous schemes such as ``javascript:``, ``vbscript:`` or
        generic ``data:`` URLs.

    Returns
    -------
    bool
        * ``True``  – if a dangerous scheme is present.
        * ``False`` – otherwise.

    Notes
    -----
    - The check is case‑insensitive.
    - ``data:image/...`` URLs are considered safe and ignored.
    - If the input is not a string, ``False`` is returned to avoid raising an exception.
    """
    if not isinstance(url_str, str):
        return False

    # Normalise the string: strip leading/trailing whitespace
    text = url_str.strip()

    # Fast path: if the string is a safe image data URL, no danger.
    if re.match(r'(?i)^data:image/', text):
        return False

    # Detect the dangerous schemes.
    # 1. javascript: or vbscript:
    if re.search(r'(?i)\b(?:javascript|vbscript):', text):
        return True

    # 2. Generic data: URL that is not an image (already filtered above)
    if re.search(r'(?i)\bdata:', text):
        return True

    # No dangerous scheme found.
    return False