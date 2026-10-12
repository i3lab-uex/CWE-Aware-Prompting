import typing

# Global dictionary that maps document URLs to their expected cryptographic signatures.
DOCUMENT_SIGNATURES: dict[str, str] = {
    # Example entries (replace with real values)
    "https://example.com/doc1.pdf": "a1b2c3d4e5f6g7h8i9j0",
    "https://example.com/doc2.pdf": "1234567890abcdef",
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
        True if the provided signature matches the stored signature; False otherwise.

    Raises
    ------
    IOError
        If the document at the specified URL cannot be found in the signature store.
    """
    # Retrieve the expected signature for the given URL.
    try:
        expected_signature = DOCUMENT_SIGNATURES[url]
    except KeyError as exc:
        raise IOError(f"Document not found or signature unavailable for URL: {url}") from exc

    # Perform a constant‑time comparison to mitigate timing attacks.
    # Python's `hmac.compare_digest` is suitable for this purpose.
    import hmac
    return hmac.compare_digest(doc_signature, expected_signature)