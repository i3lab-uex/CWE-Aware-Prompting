import hmac

# Example global mapping of URLs to their correct signatures.
# In a real system this would be securely loaded from a trusted source.
DOCUMENT_SIGNATURES = {
    "https://example.com/doc1.pdf": "a3f5c2e7b9d8...",
    "https://example.com/doc2.pdf": "4e1a6b9c3d7f...",
    # ... more entries ...
}

def validate_document(file_url: str, crypt_signature: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the stored
    signature for a given document URL.

    Parameters
    ----------
    file_url : str
        The URL of the remote document.
    crypt_signature : str
        The signature to validate.

    Returns
    -------
    bool
        True if the signatures match, False otherwise.

    Raises
    ------
    IOError
        If the document URL is not present in DOCUMENT_SIGNATURES.
    """
    if not isinstance(file_url, str):
        raise TypeError("file_url must be a string")
    if not isinstance(crypt_signature, str):
        raise TypeError("crypt_signature must be a string")

    # Retrieve the expected signature for this URL
    try:
        expected_signature = DOCUMENT_SIGNATURES[file_url]
    except KeyError as exc:
        raise IOError(f"Document not found: {file_url}") from exc

    # Use constant‑time comparison to avoid timing attacks
    return hmac.compare_digest(crypt_signature, expected_signature)