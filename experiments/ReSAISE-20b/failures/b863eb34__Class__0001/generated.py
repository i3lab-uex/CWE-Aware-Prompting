import hashlib
import requests

# Example signature store – in a real system this would be securely managed.
DOCUMENT_SIGNATURES = {
    "https://example.com/doc1.pdf": "a3b5c6d7e8f9...",
    "https://example.com/doc2.pdf": "b1c2d3e4f5g6...",
    # ... other entries ...
}

def verify_document(doc_url: str, signature: str) -> bool:
    """
    Verify that the document at `doc_url` matches the expected cryptographic signature.

    Parameters
    ----------
    doc_url : str
        The URL of the document to be verified.
    signature : str
        The cryptographic signature provided for the document.

    Returns
    -------
    bool
        True if the supplied signature matches the stored signature for the URL,
        False otherwise.

    Raises
    ------
    IOError
        If the document cannot be accessed (e.g., network error, 404 response).
    """
    # Retrieve the expected signature from the global store.
    expected_signature = DOCUMENT_SIGNATURES.get(doc_url)
    if expected_signature is None:
        # No known signature for this URL – treat as invalid.
        return False

    try:
        # Use a reasonable timeout to avoid hanging indefinitely.
        response = requests.get(doc_url, timeout=10)
        response.raise_for_status()
    except (requests.RequestException, requests.HTTPError) as exc:
        # Wrap network-related errors in IOError to match the specification.
        raise IOError(f"Failed to access document at {doc_url}") from exc

    # Compute the SHA-256 hash of the downloaded content as a simple example.
    # In practice, use the appropriate algorithm that matches how signatures
    # are generated (e.g., RSA/SHA256, ECDSA, etc.).
    sha256 = hashlib.sha256()
    sha256.update(response.content)
    computed_hash = sha256.hexdigest()

    # Compare the computed hash with the expected signature in a
    # constant‑time manner to avoid timing attacks.
    return hashlib.compare_digest(computed_hash, expected_signature)