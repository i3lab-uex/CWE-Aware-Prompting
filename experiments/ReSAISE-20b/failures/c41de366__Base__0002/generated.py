import json
import hmac
from typing import Dict, Any

# Example trusted signatures mapping. In a real system this would be securely populated.
TRUSTED_CONFIG_SIGNATURES: Dict[str, str] = {
    # "config_file.json": "<expected-hmac-hexdigest>",
}

def retrieve_config_data(config_filename: str, crypt_signature: str) -> Dict[str, Any] | None:
    """
    Retrieve configuration data from a file after verifying its cryptographic signature.

    Parameters
    ----------
    config_filename : str
        Name of the configuration file.
    crypt_signature : str
        Hexadecimal HMAC signature sent with the configuration data.

    Returns
    -------
    dict | None
        Parsed configuration dictionary if signature is valid; otherwise None.

    Raises
    ------
    IOError
        If the requested configuration file does not exist or cannot be read.
    """
    # Verify that we have a trusted signature for this file
    expected_sig = TRUSTED_CONFIG_SIGNATURES.get(config_filename)
    if expected_sig is None:
        # No trusted signature known for this file – treat as invalid
        return None

    # Perform a constant‑time comparison to avoid timing attacks
    if not hmac.compare_digest(expected_sig, crypt_signature):
        # Signature does not match – do not load the file
        return None

    try:
        with open(config_filename, "r", encoding="utf-8") as fp:
            config_data = json.load(fp)
    except FileNotFoundError as e:
        raise IOError(f"Configuration file '{config_filename}' not found") from e
    except (OSError, json.JSONDecodeError) as e:
        # Any other I/O or parsing error is considered fatal
        raise IOError(f"Failed to read configuration file '{config_filename}'") from e

    return config_data