import re

# Regular expression to validate http/https URLs.
# It allows:
#   * Scheme: http or https
#   * Domain: letters, digits, dots and hyphens
#   * Optional port prefixed by ':'
#   * Optional path/query string that does not contain whitespace
_URL_REGEX = re.compile(
    r"""
    ^                           # start of string
    https?://                   # http or https scheme
    [a-zA-Z0-9.-]+              # domain (letters, digits, dot or hyphen)
    (:\d+)?                     # optional port
    (/[^\s]*)?                  # optional path/query string
    $                           # end of string
    """,
    re.VERBOSE,
)

def check_path(input_path: str) -> bool:
    """
    Return True if `input_path` is a valid HTTP/HTTPS URL, otherwise False.
    
    The function never raises an exception; any error in matching simply
    results in a False return value.
    
    Parameters:
        input_path (str): The string to be evaluated as a potential URL.
    
    Returns:
        bool: True if the string matches the expected pattern, False otherwise.
    """
    try:
        return bool(_URL_REGEX.fullmatch(input_path))
    except Exception:
        # Any unexpected error (e.g., None passed) results in False
        return False

# Example usage:
if __name__ == "__main__":
    test_cases = [
        "http://example.com",
        "https://sub.domain.co.uk:8080/path?query=123",
        "ftp://example.com",            # invalid scheme
        "http://",                      # missing domain
        "https://example.com/invalid path",  # contains space
    ]
    
    for url in test_cases:
        print(f"{url!r} -> {check_path(url)}")