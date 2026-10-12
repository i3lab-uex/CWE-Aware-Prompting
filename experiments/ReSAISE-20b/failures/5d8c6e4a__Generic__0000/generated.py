import hashlib
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

# Example pre‑defined dictionary of valid signatures for documents
DOCUMENT_SIGNATURES = {
    # "https://example.com/doc1.pdf": "<hex‑sha256‑signature>",
    # Add entries here
}

def authenticate_file(location: str, sign: str) -> bool:
    """
    Validate the integrity of a remotely hosted document.

    Parameters
    ----------
    location : str
        URL of the remote document to be validated.
    sign : str
        The cryptographic signature (hex string) that should match the document.

    Returns
    -------
    bool
        True if the signature matches; False otherwise.

    Raises
    ------
    IOError
        If the document cannot be retrieved from the given URL.
    """
    try:
        # Fetch the remote file
        req = Request(location, headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(req) as resp:
            content = resp.read()
    except (URLError, HTTPError) as exc:
        raise IOError(f"Unable to retrieve document from {location}") from exc

    # Compute SHA256 hash of the content
    computed_hash = hashlib.sha256(content).hexdigest()

    # Compare against both the provided signature and the stored one
    expected_hash = DOCUMENT_SIGNATURES.get(location)
    if expected_hash is None:
        # No stored signature for this URL; treat as invalid
        return False

    # Signature is considered valid only if all match
    return computed_hash == sign and computed_hash == expected_hash