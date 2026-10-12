import hmac

# Global dictionary containing the valid signatures for each document URL.
# Example:
# DOCUMENT_SIGNATURES = {
#     "https://example.com/doc1.pdf": "a1b2c3d4e5f6...",
#     ...
# }
DOCUMENT_SIGNATURES = {}

def authenticate_document(url: str, doc_signature: str) -> bool:
    """
    Verify that the supplied cryptographic signature matches the stored
    signature for the document located at `url`.

    Parameters
    ----------
    url : str
        The URL of the document to validate.
    doc_signature : str
        The cryptographic signature that is provided for verification.

    Returns
    -------
    bool
        True if the provided signature corresponds to the stored signature,
        False otherwise.

    Raises
    ------
    IOError
        If no signature is found for the supplied URL (document not found).
    """
    # Retrieve the stored signature for the requested document.
    stored_sig = DOCUMENT_SIGNATURES.get(url)

    if stored_sig is None:
        # The document (or its signature) does not exist in the registry.
        raise IOError(f"Document at URL '{url}' could not be found.")

    # Use hmac.compare_digest for a timing‑attack resistant comparison.
    return hmac.compare_digest(stored_sig, doc_signature)