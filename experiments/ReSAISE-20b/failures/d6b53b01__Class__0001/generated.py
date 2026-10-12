import hashlib
import hmac
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

# Pre‑defined dictionary of authentic signatures for remote documents.
# Example format: {"https://example.com/file.txt": "abc123..."}
DOCUMENT_SIGNATURES = {
    # Populate with real signatures in production
}

def _compute_signature(data: bytes, algorithm: str = "sha256") -> str:
    """
    Compute the hex digest of *data* using the specified hashing algorithm.
    """
    hash_func = hashlib.new(algorithm)
    hash_func.update(data)
    return hash_func.hexdigest()


def check_file(document_location: str, crypto_sign: str) -> bool:
    """
    Validate the integrity of a remote document by comparing its cryptographic
    signature with an expected value.

    Parameters
    ----------
    document_location : str
        URL of the remote document to fetch.
    crypto_sign : str
        The signature provided for validation.

    Returns
    -------
    bool
        ``True`` if the signature matches the expected value, otherwise ``False``.

    Raises
    ------
    IOError
        If the document cannot be retrieved from the given URL.
    """
    # Fetch the remote document
    try:
        req = Request(document_location, headers={"User-Agent": "check_file/1.0"})
        with urlopen(req, timeout=10) as resp:
            if resp.status != 200:
                raise IOError(f"Failed to retrieve document: HTTP {resp.status}")
            data = resp.read()
    except (URLError, HTTPError) as exc:
        raise IOError(f"Unable to fetch document from {document_location}") from exc

    # Compute the signature of the retrieved data
    computed_sig = _compute_signature(data)

    # Retrieve the expected signature from the dictionary
    expected_sig = DOCUMENT_SIGNATURES.get(document_location)

    # If no expected signature is known, reject the document
    if expected_sig is None:
        return False

    # Use constant‑time comparison to mitigate timing attacks
    return hmac.compare_digest(computed_sig, expected_sig)