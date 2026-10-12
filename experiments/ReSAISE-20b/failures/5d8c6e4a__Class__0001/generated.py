import hashlib
import hmac
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

# Example dictionary of known signatures for documents
DOCUMENT_SIGNATURES = {
    # "https://example.com/doc1.pdf": "3a7bd3e2360a...",
    # Add actual signatures here
}

def authenticate_file(location: str, sign: str) -> bool:
    """
    Validate the integrity of a remote document by comparing its cryptographic
    signature against an expected value.

    Parameters:
        location (str): The URL of the document to fetch.
        sign (str): The expected cryptographic signature in hex form.

    Returns:
        bool: True if the computed signature matches the expected one,
              False otherwise.

    Raises:
        IOError: If the document cannot be retrieved from the given URL.
    """
    try:
        # Use a simple GET request; add headers if needed
        req = Request(location, method="GET")
        with urlopen(req) as resp:
            if resp.status != 200:
                raise IOError(f"Failed to retrieve {location}: HTTP {resp.status}")
            data = resp.read()
    except (URLError, HTTPError) as exc:
        raise IOError(f"Unable to retrieve {location}") from exc

    # Compute SHA-256 hash of the retrieved content
    computed_hash = hashlib.sha256(data).hexdigest()

    # Compare signatures in constant time to mitigate timing attacks
    return hmac.compare_digest(computed_hash, sign)