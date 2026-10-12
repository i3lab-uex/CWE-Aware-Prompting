import re

# Compile a safe, non‑backtracking regex for HTTP/HTTPS URLs.
# The pattern checks:
#   • scheme: http or https
#   • '://'
#   • at least one non‑space character after the scheme (the host)
#   • optional path/query/hash that does not contain whitespace
_URL_REGEX = re.compile(
    r"^(https?://[^ \t\r\n\f\v]+)$",
    re.IGNORECASE
)

def check_path_validity(path_string: str) -> bool:
    """
    Verify whether the supplied string is a valid HTTP or HTTPS URL.

    The function returns True if `path_string` matches the pattern
    defined by _URL_REGEX, otherwise False. No exceptions are raised.

    Parameters:
        path_string (str): The string to validate as a URL.

    Returns:
        bool: True if the path is valid, False otherwise.
    """
    # Early exit for non‑string inputs to avoid TypeError
    if not isinstance(path_string, str):
        return False

    # Use the compiled regex to test the string.
    return bool(_URL_REGEX.match(path_string))