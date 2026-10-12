import requests
from urllib.parse import urlparse

# Global dictionary mapping document URLs to their correct signatures.
DOCUMENT_SIGNATURES = {
    # Example entries:
    # "https://example.com/doc1.pdf": "abc123...",
    # ...
}

def verify_document(doc_url: str, signature: str) -> bool:
    """
    Verify that a document at the given URL has a valid cryptographic signature.

    Parameters
    ----------
    doc_url : str
        The URL of the document to verify.
    signature : str
        The cryptographic signature provided for the document.

    Returns
    -------
    bool
        True if the provided signature matches the expected one, False otherwise.

    Raises
    ------
    IOError
        If the document cannot be accessed (e.g., network error, non-200 status).
    """
    # Ensure the URL uses a safe scheme (http or https) to avoid arbitrary code execution.
    parsed = urlparse(doc_url)
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Unsupported URL scheme: {parsed.scheme}")

    try:
        # Perform a HEAD request to check accessibility without downloading the full content.
        response = requests.head(doc_url, timeout=10)
    except (requests.RequestException, ValueError) as exc:
        raise IOError(f"Failed to access document at {doc_url}") from exc

    if response.status_code != 200:
        raise IOError(f"Document at {doc_url} returned status code {response.status_code}")

    # Retrieve the expected signature from the global dictionary.
    expected_sig = DOCUMENT_SIGNATURES.get(doc_url)

    # If no signature is stored for this URL, we consider it invalid.
    if expected_sig is None:
        return False

    # Compare signatures securely (constant‑time comparison to mitigate timing attacks).
    def _secure_compare(a: str, b: str) -> bool:
        if len(a) != len(b):
            return False
        result = 0
        for x, y in zip(a.encode(), b.encode()):
            result |= x ^ y
        return result == 0

    return _secure_compare(signature, expected_sig)