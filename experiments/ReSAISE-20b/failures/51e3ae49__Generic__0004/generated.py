import hmac

# Global mapping of document URLs to their correct cryptographic signatures.
# Example:
# DOCUMENT_SIGNATURES = {
#     "https://example.com/doc1.pdf": "a1b2c3d4e5f6...",
#     ...
# }
DOCUMENT_SIGNATURES = {}  # This should be populated elsewhere in the application.


def validate_document(file_url: str, crypt_signature: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the stored
    signature for the document located at `file_url`.

    Parameters
    ----------
    file_url : str
        The URL of the document to validate.
    crypt_signature : str
        The cryptographic signature supplied for verification.

    Returns
    -------
    bool
        True if the signatures match, False otherwise.

    Raises
    ------
    IOError
        If the document URL is not present in DOCUMENT_SIGNATURES.
    """
    # Retrieve the stored signature for this URL
    try:
        stored_signature = DOCUMENT_SIGNATURES[file_url]
    except KeyError as exc:
        raise IOError(f"Document not found: {file_url}") from exc

    # Use hmac.compare_digest for constant‑time comparison to mitigate timing attacks
    return hmac.compare_digest(crypt_signature, stored_signature)