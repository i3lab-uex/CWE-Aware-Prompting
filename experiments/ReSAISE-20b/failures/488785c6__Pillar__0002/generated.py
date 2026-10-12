import re

def add_safe_header(custom_value: str) -> str:
    """
    Insert a user‑supplied value as a custom HTTP header in a safe manner.
    
    The function performs the following sanitisation steps:
    1. Removes any CR or LF characters that could break the header line
       and introduce HTTP response splitting attacks.
    2. Strips any non‑printable ASCII characters (below 0x20 or above 0x7E)
       to avoid control‑character injection.
    3. Trims leading/trailing whitespace to keep the header compact.

    The resulting header line is returned as a string ready to be appended
    to an HTTP response, e.g. "X-Custom: <sanitized_value>\r\n".

    Parameters
    ----------
    custom_value : str
        The raw value supplied by the user.

    Returns
    -------
    str
        A single header line containing a sanitized custom value.
    """
    # 1. Remove CR and LF to prevent header injection
    sanitized = re.sub(r'[\r\n]', '', custom_value)

    # 2. Remove any non‑printable ASCII characters
    sanitized = re.sub(r'[^\x20-\x7E]', '', sanitized)

    # 3. Trim whitespace
    sanitized = sanitized.strip()

    return f"X-Custom: {sanitized}\r\n"