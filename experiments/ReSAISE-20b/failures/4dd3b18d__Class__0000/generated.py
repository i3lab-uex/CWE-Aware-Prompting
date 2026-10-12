import requests
import hmac

# Global dictionary containing the correct signatures for documents.
# Example: {"https://example.com/doc1.pdf": "sha256:abcd1234..."}
DOC_SIGNATURES = {}


def validate_document(file_url: str, sign: str) -> bool:
    """
    Verify that the cryptographic signature supplied for a remote document
    matches the expected value stored in DOC_SIGNATURES.

    Parameters
    ----------
    file_url : str
        URL of the document to validate.
    sign : str
        Signature supplied by the caller (e.g., a SHA‑256 hash string).

    Returns
    -------
    bool
        True if the signature matches the expected value for the document,
        False otherwise.

    Raises
    ------
    IOError
        If the document cannot be retrieved from the provided URL.
    """
    # Ensure we can reach the remote file
    try:
        resp = requests.get(file_url, timeout=5)
        resp.raise_for_status()
    except (requests.RequestException, requests.Timeout) as exc:
        raise IOError(f"Unable to access document at {file_url}") from exc

    # Retrieve the expected signature
    expected = DOC_SIGNATURES.get(file_url)
    if expected is None:
        # If we have no record of this document, treat it as invalid
        return False

    # Use constant‑time comparison to avoid timing attacks
    return hmac.compare_digest(sign, expected)