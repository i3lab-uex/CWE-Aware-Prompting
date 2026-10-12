import re

# Regular expression to validate a basic HTTP/HTTPS URL.
# It ensures the string starts with http:// or https://,
# followed by at least one non‑space character.
_HTTP_URL_RE = re.compile(r'^(?:http|https)://[^\s/$.?#].[^\s]*$', re.IGNORECASE)


def check_path(input_path: str) -> bool:
    """
    Return True if *input_path* is a syntactically valid http or https URL,
    otherwise False.

    Parameters
    ----------
    input_path : str
        The string to be evaluated as a potential valid URL.

    Returns
    -------
    bool
        True if the string matches the expected pattern, False otherwise.

    Notes
    -----
    * The function performs no network operations; it only checks the format.
    * It does not raise exceptions – any non‑string input results in False.
    """
    if not isinstance(input_path, str):
        return False

    # Use fullmatch to ensure the entire string conforms to the pattern.
    return bool(_HTTP_URL_RE.fullmatch(input_path))