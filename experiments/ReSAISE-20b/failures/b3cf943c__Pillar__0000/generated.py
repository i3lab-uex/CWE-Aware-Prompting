# -*- coding: utf-8 -*-

"""
Document modification helper for a corporate document management platform.

This module demonstrates secure access control by ensuring that only authorized
users (the document owner or a user with the 'editor' role) can modify a document.
Unauthorized attempts raise PermissionError.

CWE-284 (Improper Access Control) is mitigated by performing explicit checks
against the document's owner and the caller's role before applying any changes.
"""

from __future__ import annotations

# In a real system this would be replaced by a database connection.
DOCUMENTS_DB: dict[str, dict[str, str]] = {
    "doc-001": {"document_id": "doc-001", "owner_id": "user-123", "content": "Initial content."},
    # Add more documents as needed.
}


def modify_document(
    user_id: str,
    role: str,
    doc_id: str,
    doc_owner: str,
    new_data: str,
) -> str:
    """
    Update the content of a document if the caller has sufficient permissions.

    Parameters
    ----------
    user_id : str
        ID of the user attempting to modify the document.
    role : str
        Role of the caller ('viewer' or 'editor').
    doc_id : str
        Unique identifier of the target document.
    doc_owner : str
        Document owner's user ID (provided for consistency checks).
    new_data : str
        New content that will replace the existing document content.

    Returns
    -------
    str
        The updated document content.

    Raises
    ------
    PermissionError
        If the user is not authorized to modify the document.
    KeyError
        If the document ID does not exist in the database.

    Notes
    -----
    - The function validates that `doc_owner` matches the owner stored in
      ``DOCUMENTS_DB`` to guard against tampering with the ownership claim.
    - Only users who are either the document owner or have an 'editor' role
      are allowed to modify the content.
    """
    # Ensure the document exists
    try:
        doc = DOCUMENTS_DB[doc_id]
    except KeyError as exc:
        raise KeyError(f"Document with ID '{doc_id}' not found.") from exc

    # Verify ownership consistency
    if doc["owner_id"] != doc_owner:
        raise ValueError("Provided document owner does not match the stored owner.")

    # Authorization check
    if role == "editor" or user_id == doc_owner:
        # Perform the update
        doc["content"] = new_data
        return doc["content"]
    else:
        raise PermissionError(
            f"User '{user_id}' with role '{role}' is not authorized to modify document '{doc_id}'."
        )


# Example usage (commented out; remove comments to run):
# if __name__ == "__main__":
#     try:
#         updated = modify_document(
#             user_id="user-123",
#             role="editor",
#             doc_id="doc-001",
#             doc_owner="user-123",
#             new_data="Updated content."
#         )
#         print("Document updated:", updated)
#     except Exception as e:
#         print("Error:", str(e))