import re

def insert_header_with_sanitization(custom_header_value: str) -> str:
    """
    Insert a user‑supplied value into an HTTP header after sanitizing it to
    prevent CRLF injection and other unsafe characters.

    Parameters
    ----------
    custom_header_value : str
        The raw header value supplied by the user.

    Returns
    -------
    str
        A complete HTTP header line in the form:
            "X-Custom-Header: <sanitized_value>"
    """
    # Reject None or non‑string inputs early
    if not isinstance(custom_header_value, str):
        raise TypeError("custom_header_value must be a string")

    # 1. Remove any CR or LF characters to prevent header injection.
    #    Also strip leading/trailing whitespace that could be used for padding tricks.
    sanitized = re.sub(r"[\r\n]+", "", custom_header_value).strip()

    # 2. Remove any other control characters (ASCII <32) except tab, which is
    #    allowed in HTTP headers per RFC 7230.
    sanitized = re.sub(r"[^\x09\x20-\x7E]+", "", sanitized)

    # 3. Collapse multiple spaces into a single space to avoid
    #    ambiguous formatting that might be exploited.
    sanitized = re.sub(r"\s{2,}", " ", sanitized)

    # 4. Ensure the header value is not empty after sanitization.
    if not sanitized:
        raise ValueError("Header value cannot be empty after sanitization")

    # Return the final header line
    return f"X-Custom-Header: {sanitized}"