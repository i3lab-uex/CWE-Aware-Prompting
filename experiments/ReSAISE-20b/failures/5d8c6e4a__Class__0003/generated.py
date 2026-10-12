import hashlib
import hmac
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

# Pre‑defined dictionary of authentic signatures for remote documents
DOCUMENT_SIGNATURES = {
    # Example entries:
    # "https://example.com/doc1.pdf": "5f4dcc3b5aa765d61d8327deb882cf99",
    # "https://example.com/doc2.txt": "e3b0c44298fc1c149afbf4c8996fb924",
}

def _fetch_document(url: str) -> bytes:
    """
    Fetches the document from a URL. Raises IOError if retrieval fails.
    """
    try:
        req = Request(url, headers={"User-Agent": "authenticate-file/1.0"})
        with urlopen(req, timeout=10) as resp:
            return resp.read()
    except (URLError, HTTPError) as exc:
        raise IOError(f"Unable to retrieve document from {url}") from exc

def _compute_signature(data: bytes) -> str:
    """
    Computes a SHA256 hex digest of the data.
    """
    return hashlib.sha256(data).hexdigest()

def authenticate_file(location: str, sign: str) -> bool:
    """
    Validates that the remote document at `location` matches the provided
    cryptographic signature `sign`.

    Parameters:
        location (str): URL of the document.
        sign (str): Expected cryptographic signature.

    Returns:
        bool: True if the document's computed signature matches `sign`
              and that signature is present in DOCUMENT_SIGNATURES;
              False otherwise.

    Raises:
        IOError: If the document cannot be retrieved.
    """
    # Retrieve remote content
    data = _fetch_document(location)

    # Compute the signature of the fetched document
    computed_sig = _compute_signature(data)

    # Verify that the provided signature matches the computed one
    if not hmac.compare_digest(computed_sig, sign):
        return False

    # Ensure the signature is recognized as authentic for this URL
    expected_sig = DOCUMENT_SIGNATURES.get(location)
    if expected_sig is None:
        return False

    # Final constant‑time comparison against the stored authentic signature
    return hmac.compare_digest(computed_sig, expected_sig)