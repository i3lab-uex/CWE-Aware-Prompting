import re

def is_malicious_scheme(input_url: str) -> bool:
    """
    Determine whether a string contains a potentially malicious URL scheme,
    excluding safe image-based data URLs.

    Parameters
    ----------
    input_url : str
        The string to be examined for dangerous URL schemes.

    Returns
    -------
    bool
        True if a dangerous scheme is detected, False otherwise.
    """
    if not isinstance(input_url, str):
        raise TypeError("input_url must be a string")

    # Regex matches:
    #   - javascript: or vbscript: (case‑insensitive)
    #   - data: URLs that are NOT image/* schemes
    pattern = re.compile(
        r"""^\s*
            (?:                       # start non‑capturing group
                javascript:           # JavaScript scheme
              | vbscript:             # VBScript scheme
              | data:(?!image/)      # data URL that is NOT an image
            )
        """,
        re.IGNORECASE | re.VERBOSE,
    )

    return bool(pattern.search(input_url))