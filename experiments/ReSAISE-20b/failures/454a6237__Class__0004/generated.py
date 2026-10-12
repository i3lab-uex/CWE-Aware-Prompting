import re

# Compile a simple, non‑backtracking pattern that matches http or https URLs.
_URL_PATTERN = re.compile(
    r'^https?://'                      # scheme
    r'[^\s/$.?#]'                     # first character after the scheme (not a space or special char)
    r'[^\s]*$'                        # remaining characters must not contain whitespace
)

def check_path_validity(path_string: str) -> bool:
    """
    Return True if *path_string* is a syntactically valid http or https URL
    according to the compiled regular expression, otherwise False.
    
    The function never raises an exception: any input that is not a string
    or fails to match the pattern simply returns False.
    """
    if not isinstance(path_string, str):
        return False
    # Use fullmatch to ensure the entire string satisfies the pattern.
    return bool(_URL_PATTERN.fullmatch(path_string))