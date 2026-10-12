import json
import os
import hmac

# Global dictionary mapping trusted signatures to config file names.
# In a real system this would be loaded from a secure source or embedded in the binary.
TRUSTED_CONFIG_SIGNATURES = {
    # Example entries:
    # "a1b2c3d4e5f6g7h8i9j0": "config1.json",
    # "1234567890abcdef1234": "config2.yaml",
}

def verify_config_data(config_file: str, provided_signature: str) -> dict | None:
    """
    Retrieve configuration data from *config_file* and verify that the
    provided cryptographic signature matches a trusted value.

    Parameters:
        config_file (str): Name of the configuration file to load.
        provided_signature (str): Signature string supplied alongside the data.

    Returns:
        dict: Parsed configuration content if the signature is valid.
        None: If the signature does not match any trusted entry.

    Raises:
        IOError: If the requested configuration file cannot be found or read.
    """
    # Ensure the signature is a valid hex string (basic sanity check)
    try:
        bytes.fromhex(provided_signature)
    except ValueError:
        # Malformed signature; treat as invalid
        return None

    # Verify the signature against the trusted mapping.
    # Use hmac.compare_digest to mitigate timing attacks.
    expected_file = None
    for sig, fname in TRUSTED_CONFIG_SIGNATURES.items():
        if hmac.compare_digest(sig.lower(), provided_signature.lower()):
            expected_file = fname
            break

    if expected_file is None:
        # Signature not recognized
        return None

    # The signature must correspond to the requested file.
    if expected_file != config_file:
        return None

    # Load and parse the configuration file.
    try:
        with open(config_file, "r", encoding="utf-8") as fp:
            # Assume JSON format; adjust if other formats are needed.
            config_data = json.load(fp)
    except FileNotFoundError:
        raise IOError(f"Configuration file '{config_file}' not found.")
    except json.JSONDecodeError as exc:
        # Malformed JSON; treat as invalid
        raise IOError(f"Configuration file '{config_file}' contains invalid JSON: {exc}")

    return config_data