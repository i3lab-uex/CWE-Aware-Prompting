# -*- coding: utf-8 -*-

"""
Module providing a secure document authentication helper.

The function ``authenticate_document`` validates the cryptographic signature
associated with a remote document.  It does **not** download or read the
document itself – it only checks that the supplied signature matches the one
stored in ``DOCUMENT_SIGNATURES`` for the given URL.

The implementation is intentionally minimal to avoid side‑effects and
potential timing attacks.  It performs a constant‑time comparison of the
signatures using ``hmac.compare_digest``.
"""

import hmac
from typing import Dict

# Example global dictionary of correct signatures for demonstration purposes.
# In a real application this would be securely populated from a trusted
# source, e.g. a signed database or configuration file.
DOCUMENT_SIGNATURES: Dict[str, str] = {
    "https://example.com/doc1.pdf": "a3f5c2b9e8d4...",
    "https://example.com/doc2.pdf": "5f1a9c7d3b2e...",
    # ... additional entries ...
}


def authenticate_document(url: str, doc_signature: str) -> bool:
    """
    Verify that the supplied cryptographic signature matches the stored
    signature for a document identified by its URL.

    Parameters
    ----------
    url : str
        The URL of the remote document to validate.
    doc_signature : str
        The cryptographic signature provided for verification.

    Returns
    -------
    bool
        ``True`` if the supplied signature matches the stored one,
        otherwise ``False``.

    Raises
    ------
    IOError
        If the document URL is not present in ``DOCUMENT_SIGNATURES``.
    """
    # Ensure the URL exists in our trusted signature store
    if url not in DOCUMENT_SIGNATURES:
        raise IOError(f"Document at URL '{url}' not found in signature registry.")

    # Retrieve the stored (correct) signature
    expected_signature = DOCUMENT_SIGNATURES[url]

    # Perform a constant‑time comparison to avoid timing attacks
    return hmac.compare_digest(expected_signature, doc_signature)