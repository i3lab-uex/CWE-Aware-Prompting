import requests
from urllib.parse import urlparse

# Predefined mapping of document URLs to their legitimate cryptographic signatures.
# In a real system this would be populated from a secure source or configuration file.
DOCUMENT_SIGNATURES = {
    # Example: "https://example.com/doc1.pdf": "sha256-hash-value"
}

def validate_file(url: str, crypt_signature: str) -> bool:
    """
    Validate the integrity of a remotely hosted document.

    Parameters
    ----------
    url : str
        The URL of the remote document to be verified.
    crypt_signature : str
        The cryptographic signature supplied for validation.

    Returns
    -------
    bool
        True if the provided signature matches the stored signature for this URL,
        False otherwise.

    Raises
    ------
    IOError
        If the document cannot be retrieved from the given URL.
    """
    # Sanity check: ensure URL is absolute and has a valid scheme
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        raise IOError(f"Invalid URL: {url}")

    # Retrieve the document to confirm it is reachable.
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except (requests.RequestException, requests.HTTPError) as exc:
        # Wrap any request-related exception in IOError for consistency.
        raise IOError(f"Failed to retrieve document from {url}") from exc

    # Fetch the expected signature for this URL.
    expected_signature = DOCUMENT_SIGNATURES.get(url)
    if expected_signature is None:
        # If we don't have a known signature for this URL, treat it as invalid.
        return False

    # Compare the provided signature with the expected one in a timing-attack safe manner.
    return _constant_time_compare(crypt_signature, expected_signature)


def _constant_time_compare(val1: str, val2: str) -> bool:
    """
    Compare two strings in constant time to mitigate timing attacks.
    """
    if len(val1) != len(val2):
        return False
    result = 0
    for x, y in zip(val1.encode(), val2.encode()):
        result |= x ^ y
    return result == 0