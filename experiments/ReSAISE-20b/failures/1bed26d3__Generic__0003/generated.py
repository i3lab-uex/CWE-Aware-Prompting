import re

def check_javascript_scheme(url_str: str) -> bool:
    """
    Detects whether a string contains a potentially dangerous URL scheme,
    excluding safe image-based data URLs.

    Parameters
    ----------
    url_str : str
        The URL or string to inspect.

    Returns
    -------
    bool
        ``True`` if the string contains a dangerous scheme (javascript:, vbscript:)
        or a data: URL that is *not* an image; ``False`` otherwise.
    """
    if not isinstance(url_str, str):
        return False

    # Normalize leading whitespace and case
    s = url_str.lstrip().lower()

    # 1. Direct dangerous schemes
    if s.startswith('javascript:') or s.startswith('vbscript:'):
        return True

    # 2. Data URLs – allow only image/* MIME types
    if s.startswith('data:'):
        # Grab everything up to the first ';' or ',' after 'data:'
        payload = s[5:]  # strip 'data:'
        sep_index = min(
            (payload.find(';') if ';' in payload else len(payload)),
            (payload.find(',') if ',' in payload else len(payload))
        )
        mime_type = payload[:sep_index]
        # If no MIME type specified, assume text/plain (dangerous)
        if not mime_type:
            return True
        # If MIME type starts with 'image/' → safe
        if mime_type.startswith('image/'):
            return False
        # Any other MIME type → dangerous
        return True

    return False