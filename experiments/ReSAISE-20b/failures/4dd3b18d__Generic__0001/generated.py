import requests
import hmac

# Global dictionary containing the expected signatures for each document URL.
# Example:
# DOC_SIGNATURES = {
#     "https://example.com/docs/report.pdf": "a1b2c3d4e5f6g7h8i9j0",
#     ...
# }
DOC_SIGNATURES = {}

def validate_document(file_url: str, sign: str) -> bool:
    """
    Validate the cryptographic signature of a document hosted at `file_url`.

    Parameters
    ----------
    file_url : str
        The URL of the document to validate.
    sign : str
        The cryptographic signature submitted with the document.

    Returns
    -------
    bool
        True if the provided signature matches the expected value for the document,
        False otherwise.

    Raises
    ------
    IOError
        If the document at `file_url` cannot be accessed (e.g., network error, 404).
    """
    # Verify that we have a signature for this URL
    expected_sign = DOC_SIGNATURES.get(file_url)
    if expected_sign is None:
        # No known signature for this URL – treat as invalid
        return False

    try:
        # Attempt to fetch the document to confirm accessibility.
        # A small timeout is used; adjust as needed.
        response = requests.get(file_url, timeout=5)
        response.raise_for_status()
    except (requests.RequestException, requests.HTTPError) as exc:
        # Any problem accessing the document is considered an IOError.
        raise IOError(f"Unable to access document at {file_url}") from exc

    # Use a constant‑time comparison to mitigate timing attacks.
    return hmac.compare_digest(sign, expected_sign)