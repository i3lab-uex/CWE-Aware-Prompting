import re

def verify_javascript_protocol(url_input: str) -> bool:
    """
    Detects potentially dangerous URL schemes in the given string.

    A URL is considered harmful if it starts with a scheme such as
    `javascript:` or `vbscript:`, or any other non‑image data scheme.
    Image data URLs (`data:image/...`) are considered safe.

    Parameters
    ----------
    url_input : str
        The URL string to inspect.

    Returns
    -------
    bool
        True if a harmful scheme is detected, False otherwise.
    """
    # Normalize the input: strip leading/trailing whitespace and lower‑case
    url = url_input.strip().lower()

    # Regex to capture the scheme at the start of the string
    scheme_match = re.match(r'^(?P<scheme>[a-z]+):', url)
    if not scheme_match:
        # No scheme found – treat as safe
        return False

    scheme = scheme_match.group('scheme')

    # Image data URLs are explicitly allowed
    if scheme == 'data':
        # Allow only `data:image/...` URLs
        return not re.match(r'^data\s*:\s*image/', url)

    # Any other scheme is considered potentially harmful
    return True