import requests
from typing import Dict

# Global dictionary mapping document URLs to their expected signatures.
DOCUMENT_SIGNATURES: Dict[str, str] = {
    # Example entries; replace with actual data in production.
    "https://example.com/doc1.pdf": "abc123def456",
    "https://example.com/report.txt": "789xyz012345",
}

def verify_document(doc_url: str, signature: str) -> bool:
    """
    Verify that the cryptographic signature for a remote document matches
    the expected value stored in DOCUMENT_SIGNATURES.

    Parameters
    ----------
    doc_url : str
        The URL of the document to verify.
    signature : str
        The cryptographic signature provided for the document.

    Returns
    -------
    bool
        True if the supplied signature matches the expected one; False otherwise.

    Raises
    ------
    IOError
        If the document cannot be accessed (network error, HTTP error,
        or any other issue while retrieving the resource).
    """
    # First ensure we can reach the document. We only need to confirm
    # accessibility, not download its contents.
    try:
        response = requests.head(doc_url, timeout=10)
        # Raise an HTTPError for bad status codes (e.g., 404, 500).
        response.raise_for_status()
    except requests.exceptions.RequestException as exc:
        # Convert any network-related exception into an IOError.
        raise IOError(f"Unable to access document at {doc_url}") from exc

    # Retrieve the expected signature from the global dictionary.
    expected_signature = DOCUMENT_SIGNATURES.get(doc_url)

    # If no signature is known for this URL, treat it as invalid.
    if expected_signature is None:
        return False

    # Compare the provided signature to the expected one.
    # Use a constant‑time comparison to avoid timing attacks if
    # signatures are large or sensitive.
    return _constant_time_compare(signature, expected_signature)


def _constant_time_compare(a: str, b: str) -> bool:
    """
    Compare two strings in constant time to mitigate timing attacks.
    """
    if len(a) != len(b):
        return False
    result = 0
    for x, y in zip(a.encode("utf-8"), b.encode("utf-8")):
        result |= x ^ y
    return result == 0