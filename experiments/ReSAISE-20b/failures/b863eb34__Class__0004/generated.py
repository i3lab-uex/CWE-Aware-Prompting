import requests

# Global dictionary mapping document URLs to their correct signatures.
DOCUMENT_SIGNATURES = {
    # Example entries:
    # "https://example.com/doc1.pdf": "abcd1234efgh5678",
    # "https://example.org/report.txt": "deadbeefcafe1234",
}

def verify_document(doc_url: str, signature: str) -> bool:
    """
    Verify the authenticity of a remote document by comparing its cryptographic
    signature with the expected value stored in DOCUMENT_SIGNATURES.

    Parameters:
        doc_url (str): The URL of the document to verify.
        signature (str): The cryptographic signature provided for the document.

    Returns:
        bool: True if the signature matches the stored value, False otherwise.

    Raises:
        IOError: If the document cannot be accessed (network error or HTTP status
                 code indicating failure).
    """
    # First, ensure we can reach the document.
    try:
        response = requests.get(doc_url, timeout=10)
        response.raise_for_status()  # Raises HTTPError for bad status codes
    except requests.exceptions.RequestException as exc:
        # Wrap any request-related exception into an IOError to match the spec.
        raise IOError(f"Failed to access document at {doc_url}") from exc

    # Retrieve the expected signature for this URL, if any.
    expected_sig = DOCUMENT_SIGNATURES.get(doc_url)

    # If we don't have a stored signature for this URL, treat it as invalid.
    if expected_sig is None:
        return False

    # Compare signatures in a constant‑time manner to avoid timing attacks.
    def _constant_time_compare(a: str, b: str) -> bool:
        if len(a) != len(b):
            return False
        result = 0
        for x, y in zip(a.encode(), b.encode()):
            result |= x ^ y
        return result == 0

    return _constant_time_compare(signature, expected_sig)