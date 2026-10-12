import re

def include_custom_header(custom_value: str) -> str:
    """
    Insert a custom header into an HTTP response, sanitizing the user-provided value
    to prevent injection attacks (CWE-74).

    The function uses a regular expression that removes any character not allowed
    in an HTTP token as defined by RFC 7230. This ensures that the header value
    cannot break out of its intended context or inject new headers.

    Parameters:
        custom_value (str): The raw value supplied by the user for the header.

    Returns:
        str: A fully-formed header string, e.g. "X-Custom-Header: sanitized_value".
    """
    # RFC 7230 token characters: any CHAR except CTLs or separators
    # Separators: ()<>@,;:\\\"/[]?={} \t
    # We allow the standard token characters and a subset of safe punctuation.
    allowed_pattern = re.compile(r'[^A-Za-z0-9!#$%&\'*+\-.^_`|~]')
    sanitized = allowed_pattern.sub('', custom_value).strip()

    # Ensure the header value is not empty after sanitization
    if not sanitized:
        raise ValueError("Custom header value must contain at least one valid character.")

    return f"X-Custom-Header: {sanitized}"