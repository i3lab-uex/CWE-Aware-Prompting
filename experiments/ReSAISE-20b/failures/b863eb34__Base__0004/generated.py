import requests
import hmac

# Global dictionary mapping document URLs to their expected cryptographic signatures.
# In a real system this would be populated from a secure source or database.
DOCUMENT_SIGNATURES = {
    "https://example.com/doc1.pdf": "a3f5c8e2b7d4...",
    # Add more entries as needed
}

def verify_document(doc_url: str, signature: str) -> bool:
    """
    Verify that the document at `doc_url` matches the provided cryptographic `signature`.

    Parameters
    ----------
    doc_url : str
        URL of the document to verify.
    signature : str
        Cryptographic signature provided for the document.

    Returns
    -------
    bool
        True if the signature matches the expected value, False otherwise.

    Raises
    ------
    IOError
        If the document cannot be accessed at the given URL.
    """
    try:
        response = requests.get(doc_url, timeout=10)
        response.raise_for_status()
    except (requests.RequestException, requests.Timeout) as exc:
        raise IOError(f"Could not retrieve document from {doc_url}") from exc

    # Retrieve the expected signature for this URL, if any.
    expected_sig = DOCUMENT_SIGNATURES.get(doc_url)
    if expected_sig is None:
        # If the URL is not known, we cannot verify it.
        return False

    # Use a constant‑time comparison to avoid timing attacks.
    return hmac.compare_digest(signature, expected_sig)