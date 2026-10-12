import hashlib
import hmac
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

# Pre‑defined dictionary mapping URLs to their authentic signatures.
DOCUMENT_SIGNATURES = {
    # Example entries:
    # "https://example.com/doc1.pdf": "5f2d...a1b",
    # "https://example.com/doc2.pdf": "3c9e...f4d",
}


def _retrieve_document(url: str) -> bytes:
    """
    Retrieve the content of a remote document.

    Raises IOError if the resource cannot be fetched.
    """
    try:
        req = Request(url, headers={"User-Agent": "check_file/1.0"})
        with urlopen(req) as resp:
            return resp.read()
    except (URLError, HTTPError) as exc:
        raise IOError(f"Unable to retrieve document from {url}") from exc


def _compute_signature(data: bytes, algorithm: str = "sha256") -> str:
    """
    Compute the hexadecimal digest of *data* using the specified algorithm.
    """
    hash_func = hashlib.new(algorithm)
    hash_func.update(data)
    return hash_func.hexdigest()


def check_file(document_location: str, crypto_sign: str) -> bool:
    """
    Validate that *crypto_sign* matches the authentic signature for
    the document located at *document_location*.

    Parameters
    ----------
    document_location : str
        URL of the remote document.
    crypto_sign : str
        Cryptographic signature supplied for verification.

    Returns
    -------
    bool
        True if the signature is correct, False otherwise.

    Raises
    ------
    IOError
        If the document cannot be retrieved from the given URL.
    """
    # 1. Retrieve the document
    content = _retrieve_document(document_location)

    # 2. Compute its signature (using the same algorithm as stored)
    computed_sig = _compute_signature(content)

    # 3. Fetch the expected signature from the dictionary
    expected_sig = DOCUMENT_SIGNATURES.get(document_location)

    # If no expected signature is known, consider verification failed
    if expected_sig is None:
        return False

    # 4. Perform a timing‑safe comparison
    return hmac.compare_digest(computed_sig, expected_sig)