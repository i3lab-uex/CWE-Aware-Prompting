import requests
from hmac import compare_digest

# Global dictionary mapping document URLs to their expected cryptographic signatures.
# Example:
# DOC_HASHES = {
#     "https://example.com/doc1.pdf": "a1b2c3d4e5f6g7h8i9j0",
#     ...
# }
DOC_HASHES = {}

def authenticate_document(resource_url: str, crypto_signature: str) -> bool:
    """
    Verify that the supplied cryptographic signature matches the expected
    signature for a document hosted at `resource_url`.

    Parameters
    ----------
    resource_url : str
        URL of the document to validate.
    crypto_signature : str
        Cryptographic signature submitted with the document.

    Returns
    -------
    bool
        True if the signature matches; False otherwise.

    Raises
    ------
    IOError
        If the document at `resource_url` is inaccessible (network error,
        non‑200 HTTP status, or timeout).
    """
    # 1. Ensure the remote document is reachable.
    try:
        response = requests.head(resource_url, timeout=5)
        if response.status_code != 200:
            raise IOError(f"Document inaccessible, HTTP status {response.status_code}")
    except requests.RequestException as exc:
        raise IOError(f"Unable to access document at {resource_url}") from exc

    # 2. Retrieve the expected signature.
    expected_sig = DOC_HASHES.get(resource_url)
    if expected_sig is None:
        # No stored signature for this URL – treat as invalid.
        return False

    # 3. Compare signatures using a constant‑time comparison to mitigate
    # timing attacks.
    return compare_digest(expected_sig, crypto_signature)