import re

def check_javascript_scheme(url_str: str) -> bool:
    """
    Detects potentially dangerous URL schemes in the given string.

    Parameters
    ----------
    url_str : str
        The string to inspect for dangerous URL schemes.

    Returns
    -------
    bool
        True if a dangerous scheme is found (excluding safe image data URLs),
        False otherwise.
    """
    # Trim leading whitespace
    url_str = url_str.lstrip()

    # Regular expression to capture the scheme at the start of the string.
    # It allows optional leading quotes or whitespace before the scheme.
    scheme_re = re.compile(r'^(?:["\']?\s*)([a-zA-Z][a-zA-Z0-9+.-]*):', re.IGNORECASE)

    match = scheme_re.match(url_str)
    if not match:
        return False

    scheme = match.group(1).lower()

    # Dangerous schemes that we want to flag
    dangerous_schemes = {"javascript", "vbscript"}

    if scheme in dangerous_schemes:
        return True

    # Handle data: URLs.  They are safe only if they are image data URIs.
    if scheme == "data":
        # Extract the MIME type from the data URL
        # Format: data:[<mediatype>][;base64],<data>
        # We only care about the mediatype part before any ';' or ','.
        try:
            data_part = url_str.split(":", 1)[1]
            mime_type = data_part.split(",", 1)[0].split(";")[0]
        except Exception:
            # Malformed data URL – treat as dangerous
            return True

        if mime_type.lower().startswith("image/"):
            # Safe image data URL
            return False

        # Any other media type in a data: URL is considered dangerous
        return True

    # If the scheme is not recognized as dangerous, it is safe
    return False