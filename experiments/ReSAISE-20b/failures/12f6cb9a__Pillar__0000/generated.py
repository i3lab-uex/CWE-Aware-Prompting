import hashlib
import hmac
from urllib.request import Request, urlopen, HTTPError

# Global dictionary containing the correct signatures for documents.
# Example format: {"https://example.com/doc1.pdf": "sha256hexsignature", ...}
DOCUMENT_SIGNATURES = {
    # Populate with actual document URLs and their SHA‑256 signatures
}

def authenticate_document(url: str, doc_signature: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the stored
    signature for a document located at ``url``.

    Parameters
    ----------
    url : str
        The URL of the document to validate.
    doc_signature : str
        The cryptographic signature supplied for verification.

    Returns
    -------
    bool
        ``True`` if the supplied signature matches the stored one,
        otherwise ``False``.

    Raises
    ------
    IOError
        If the document cannot be located (e.g., 404 Not Found).
    """
    # First, ensure the document exists on the remote server
    req = Request(url, method='HEAD')
    try:
        with urlopen(req) as resp:
            # Any 2xx or 3xx status code is considered a valid document
            if resp.status >= 400:
                raise IOError(f"Document at {url} not found (HTTP {resp.status}).")
    except HTTPError as e:
        if e.code == 404:
            raise IOError(f"Document at {url} not found (HTTP 404).") from e
        raise IOError(f"Failed to access document at {url} (HTTP {e.code}).") from e
    except Exception as exc:
        raise IOError(f"Unable to reach {url}: {exc}") from exc

    # Retrieve the stored signature for this URL
    expected_sig = DOCUMENT_SIGNATURES.get(url)
    if expected_sig is None:
        # If we don't have a stored signature, treat it as invalid
        return False

    # Perform a constant‑time comparison to avoid timing attacks
    try:
        # Ensure both signatures are in the same format (hex string)
        return hmac.compare_digest(expected_sig.lower(), doc_signature.lower())
    except Exception:
        # If comparison fails for any reason, consider the signature invalid
        return False