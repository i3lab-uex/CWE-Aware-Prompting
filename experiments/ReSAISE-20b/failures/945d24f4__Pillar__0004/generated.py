# ──────────────────────────────────────────────────────────────────────── #
#  update_car_information.py                                               #
#  Author: ChatGPT                                                         #
#  Description: Safely updates a vehicle's details based on allowed fields.#
# ──────────────────────────────────────────────────────────────────────── #

from typing import Dict, Any

# Global list of fields that are permitted to be updated
ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "color",
    "vin",
    "mileage",
]

def update_car_information(
    car_details: Dict[str, Any], changes: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Update a vehicle's details in a safe manner.

    Parameters
    ----------
    car_details : dict
        The original dictionary containing the vehicle's properties.
    changes : dict
        Dictionary with keys to be updated and their new values.

    Returns
    -------
    dict
        A new dictionary reflecting the updates after applying only
        changes that are present in ALLOWED_FIELDS.

    Raises
    ------
    TypeError
        If either `car_details` or `changes` is not a dictionary.
    ValueError
        If any key in `changes` is not in ALLOWED_FIELDS.

    Notes
    -----
    - The function does **not** modify the input `car_details` dictionary.
    - It returns a new dictionary containing the updated values.
    """
    # Validate input types
    if not isinstance(car_details, dict):
        raise TypeError("car_details must be a dictionary")
    if not isinstance(changes, dict):
        raise TypeError("changes must be a dictionary")

    # Create a shallow copy to avoid mutating the original dict
    updated = car_details.copy()

    # Apply changes only for allowed fields
    for key, value in changes.items():
        if key not in ALLOWED_FIELDS:
            raise ValueError(f"Field '{key}' is not allowed to be updated.")
        # Optional: add type or value checks here if needed
        updated[key] = value

    return updated


# ──────────────────────────────────────────────────────────────────────── #
#  Example usage (for manual testing)                                      #
# ──────────────────────────────────────────────────────────────────────── #

if __name__ == "__main__":
    original = {
        "make": "Toyota",
        "model": "Corolla",
        "year": 2015,
        "color": "Blue",
        "vin": "123ABC456DEF78901",
        "mileage": 75000,
    }

    changes = {
        "color": "Red",
        "mileage": 76000,
        # The following line would raise a ValueError:
        # "owner": "John Doe",
    }

    try:
        updated = update_car_information(original, changes)
        print("Original:", original)
        print("Updated :", updated)
    except Exception as e:
        print(f"Error: {e}")