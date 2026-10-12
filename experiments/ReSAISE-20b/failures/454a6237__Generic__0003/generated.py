import re

# Regular expression pattern to validate http or https URLs.
# It requires a scheme (http or https), followed by ://, then at least one non-whitespace character.
# The pattern is intentionally simple to avoid complex parsing while still catching common mistakes.
_HTTP_URL_PATTERN = re.compile(
    r"""
    ^                           # start of string
    (?:http|https)://           # scheme with ://
    [^\s/$.?#].[^\s]*           # at least one non-whitespace character, followed by any non-whitespace characters
    $                           # end of string
    """,
    re.IGNORECASE | re.VERBOSE,
)

def check_path_validity(path_string: str) -> bool:
    """
    Validate whether the provided string is a syntactically correct HTTP/HTTPS URL.

    Args:
        path_string (str): The string to validate as a URL.

    Returns:
        bool: True if the string matches the HTTP/HTTPS pattern, False otherwise.
    """
    try:
        # Ensure path_string is a string; if not, return False gracefully.
        if not isinstance(path_string, str):
            return False

        # Use fullmatch to require the entire string to match the pattern.
        return bool(_HTTP_URL_PATTERN.fullmatch(path_string.strip()))
    except Exception:
        # In case of unexpected errors (e.g., re module issues), return False.
        return False