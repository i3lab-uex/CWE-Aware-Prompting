import hashlib
import hmac
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError

# Global dictionary containing the expected signatures for each document URL
DOCUMENT_SIGNATURES = {
    # Example entries (replace with real data in production)
    "https://example.com/doc1.pdf": "a3f5c2e8d9b0...",
    "https://example.com/doc2.txt": "4b7e1d9c3f6a...",
    # ...
}


def _fetch_document(url: str) -> bytes:
    """
    Retrieve the raw content of a document from a remote URL.

    Parameters
    ----------
    url : str
        The URL of the document to fetch.

    Returns
    -------
    bytes
        Raw byte content of the fetched document.

    Raises
    ------
    IOError
        If the URL cannot be accessed or the resource is missing.
    """
    try:
        req = Request(url, headers={"User-Agent": "validate-document/1.0"})
        with urlopen(req) as resp:
            if resp.status != 200:
                raise IOError(f"Unexpected HTTP status {resp.status} for URL: {url}")
            return resp.read()
    except HTTPError as e:
        if e.code == 404:
            raise IOError(f"Document not found: {url}") from e
        raise IOError(f"HTTP error accessing {url}: {e}") from e
    except URLError as e:
        raise IOError(f"Unable to reach {url}: {e}") from e


def _compute_signature(content: bytes) -> str:
    """
    Compute a SHA-256 hash of the document content and return it as a hex string.

    Parameters
    ----------
    content : bytes
        The raw document data.

    Returns
    -------
    str
        Hexadecimal representation of the SHA-256 hash.
    """
    sha256 = hashlib.sha256()
    sha256.update(content)
    return sha256.hexdigest()


def validate_document(file_url: str, crypt_signature: str) -> bool:
    """
    Verify that the provided cryptographic signature matches the expected
    signature for a remote document.

    Parameters
    ----------
    file_url : str
        The URL of the document to validate.
    crypt_signature : str
        The signature supplied for verification.

    Returns
    -------
    bool
        True if the provided signature matches the expected signature,
        False otherwise.

    Raises
    ------
    IOError
        If the document at `file_url` cannot be retrieved.
    """
    # Fetch the remote document
    content = _fetch_document(file_url)

    # Compute its signature locally
    computed_sig = _compute_signature(content)

    # Retrieve the expected signature from the global mapping
    expected_sig = DOCUMENT_SIGNATURES.get(file_url)
    if expected_sig is None:
        # If we have no stored signature, treat it as a mismatch
        return False

    # Use constant‑time comparison to mitigate timing attacks (CWE‑347)
    return hmac.compare_digest(computed_sig, crypt_signature) and \
           hmac.compare_digest(computed_sig, expected_sig)