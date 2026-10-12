# -*- coding: utf-8 -*-

"""
Document management helper module.

This module contains a simple in‑memory document store and a function
to modify documents while enforcing proper authorization checks.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# In‑memory document database
# --------------------------------------------------------------------------- #

DOCUMENTS_DB: dict[str, dict[str, str]] = {
    # Example entries – in a real system these would be persisted
    "doc-001": {"document_id": "doc-001", "owner_id": "user-123", "content": "Initial content of doc 1."},
    "doc-002": {"document_id": "doc-002", "owner_id": "user-456", "content": "Initial content of doc 2."},
}

# --------------------------------------------------------------------------- #
# Utility functions
# --------------------------------------------------------------------------- #

def _is_authorized(account_id: str, account_role: str, owner_id: str) -> bool:
    """
    Determine if a user is authorized to modify a document.

    A user can modify a document if:
      * They have the 'editor' role, or
      * They are the owner of the document.

    Parameters:
        account_id (str): ID of the user attempting modification.
        account_role (str): Role of the user ('viewer', 'editor', etc.).
        owner_id (str): ID of the document's creator.

    Returns:
        bool: True if authorized, False otherwise.
    """
    return account_role.lower() == "editor" or account_id == owner_id

# --------------------------------------------------------------------------- #
# Core functionality
# --------------------------------------------------------------------------- #

def modify_file(
    account_id: str,
    account_role: str,
    file_id: str,
    owner_id: str,
    updated_content: str
) -> str:
    """
    Update the content of a document after performing authorization checks.

    Args:
        account_id (str): ID of the user attempting to modify.
        account_role (str): Role of the user ('viewer', 'editor', etc.).
        file_id (str): ID of the target document.
        owner_id (str): Expected owner ID of the document.
        updated_content (str): New content to store.

    Returns:
        str: The new content of the document if modification succeeds.

    Raises:
        ValueError: If the document ID does not exist in the system.
        PermissionError: If the user is not authorized to modify the document.
    """
    # 1. Verify that the requested file exists
    if file_id not in DOCUMENTS_DB:
        raise ValueError(f"Document with ID '{file_id}' does not exist.")

    # 2. Retrieve the document
    doc = DOCUMENTS_DB[file_id]

    # 3. Check that the owner ID matches the stored one (prevent spoofing)
    if doc["owner_id"] != owner_id:
        raise ValueError("Provided owner ID does not match the document's actual owner.")

    # 4. Perform authorization check
    if not _is_authorized(account_id, account_role, owner_id):
        raise PermissionError("User is not authorized to modify this document.")

    # 5. Apply the update safely
    doc["content"] = updated_content

    # 6. Return the new content
    return doc["content"]

# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

# if __name__ == "__main__":
#     try:
#         new_text = modify_file(
#             account_id="user-123",
#             account_role="viewer",
#             file_id="doc-001",
#             owner_id="user-123",
#             updated_content="Updated content from the viewer."
#         )
#         print("Modification succeeded:", new_text)
#     except Exception as e:
#         print("Error:", str(e))