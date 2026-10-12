import requests
import hmac

# Global dictionary mapping document URLs to their correct signatures.
DOCUMENT_SIGNATURES = {
    # Example entries
    "https://example.com/doc1.txt": "a3f5c7d9e1b2...",
    "https://example.com/doc2.pdf": "4b6d8f0e2c9a...",
    # Add more entries as needed
}

def verify_document(doc_url: str, signature: str) -> bool:
    """
    Verify the authenticity of a document located at `doc_url` by comparing
    its provided cryptographic signature against the expected one stored in
    DOCUMENT_SIGNATURES.

    Parameters
    ----------
    doc_url : str
        The URL of the document to verify.
    signature : str
        The cryptographic signature supplied for the document.

    Returns
    -------
    bool
        True if the provided signature matches the expected one, False otherwise.

    Raises
    ------
    IOError
        If the document cannot be accessed at the given URL.
    """
    # Ensure we can reach the remote document
    try:
        response = requests.head(doc_url, timeout=10)
        if response.status_code != 200:
            raise IOError(f"Unable to access document: {doc_url} (status {response.status_code})")
    except requests.RequestException as exc:
        raise IOError(f"Unable to access document: {doc_url}") from exc

    # Retrieve the expected signature
    expected_sig = DOCUMENT_SIGNATURES.get(doc_url)
    if expected_sig is None:
        # No signature known for this document
        return False

    # Use constant‑time comparison to avoid timing attacks
    return hmac.compare_digest(signature, expected_sig)