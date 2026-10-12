import re

def insert_header_with_sanitization(custom_header_value: str) -> str:
    """
    Insert a user‑supplied value into an HTTP header after sanitizing it.

    The function ensures that the value contains only printable US‑ASCII characters
    and does not contain CR or LF characters, which could otherwise be used for
    HTTP response splitting attacks (CWE‑107 and CWE‑707).

    Parameters
    ----------
    custom_header_value : str
        The raw value supplied by the user.

    Returns
    -------
    str
        A header string of the form "X-Custom-Header: <sanitized_value>".
    """
    # 1. Remove any CR or LF characters that could break the header line
    cleaned = re.sub(r'[\r\n]+', ' ', custom_header_value)

    # 2. Strip leading/trailing whitespace
    cleaned = cleaned.strip()

    # 3. Allow only printable US‑ASCII characters (0x20–0x7E)
    #    Any character outside this range is replaced with a space.
    cleaned = re.sub(r'[^\x20-\x7E]', ' ', cleaned)

    # 4. Collapse multiple spaces into a single space to avoid header injection
    cleaned = re.sub(r'\s+', ' ', cleaned)

    # 5. Construct the final header string
    return f"X-Custom-Header: {cleaned}"