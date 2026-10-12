import hmac

# Global mapping of document URLs to their expected cryptographic signatures.
# In a real system this would be securely stored and accessed (e.g., via
# a protected key-value store or database). For this example it is simply
# defined as a module-level dictionary.
DOCUMENT_SIGNATURES = {
    # Example entries:
    # "https://example.com/doc1.pdf": "abc123...",
    # ...
}

def authenticate_document(url: str, doc_signature: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for a document located at `url`.

    Parameters
    ----------
    url : str
        The URL of the document to validate.
    doc_signature : str
        The cryptographic signature supplied for verification.

    Returns
    -------
    bool
        True if the provided signature matches the stored signature,
        False otherwise.

    Raises
    ------
    IOError
        If no expected signature is found for the specified URL.
    """
    # Retrieve the expected signature from the global dictionary
    expected_sig = DOCUMENT_SIGNATURES.get(url)

    if expected_sig is None:
        # No stored signature for this URL – treat as missing document
        raise IOError(f"Document at {url} not found or has no stored signature")

    # Use hmac.compare_digest for constant-time comparison to mitigate
    # timing attacks. This ensures the operation takes the same amount of
    # time regardless of how much of the signature matches.
    return hmac.compare_digest(doc_signature, expected_sig)