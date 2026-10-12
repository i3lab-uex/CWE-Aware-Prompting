import requests

# Example global dictionary of expected signatures.
# In real usage this would be populated elsewhere in the application.
DOC_HASHES = {
    "https://example.com/doc1.pdf": "abc123def456",
    "https://example.org/report.docx": "789ghi012jkl",
}

def authenticate_document(resource_url: str, crypto_signature: str) -> bool:
    """
    Verify that a document's cryptographic signature matches the expected value.

    Parameters
    ----------
    resource_url : str
        URL of the document to validate.
    crypto_signature : str
        Cryptographic signature submitted with the document.

    Returns
    -------
    bool
        True if the signature matches the expected value for the document,
        False otherwise.

    Raises
    ------
    IOError
        If the document at `resource_url` cannot be accessed (e.g., network error,
        non‑200 HTTP status, etc.).
    """
    try:
        # Perform a lightweight HEAD request to confirm accessibility.
        response = requests.head(resource_url, timeout=5)
        if response.status_code != 200:
            raise IOError(f"Document not accessible, status code {response.status_code}")
    except requests.RequestException as exc:
        raise IOError(f"Failed to access document at {resource_url}: {exc}") from exc

    expected_sig = DOC_HASHES.get(resource_url)
    if expected_sig is None:
        # Unknown document – treat as invalid signature.
        return False

    # Use constant‑time comparison to mitigate timing attacks
    def _const_time_eq(a: str, b: str) -> bool:
        if len(a) != len(b):
            return False
        result = 0
        for x, y in zip(a.encode(), b.encode()):
            result |= x ^ y
        return result == 0

    return _const_time_eq(crypto_signature, expected_sig)