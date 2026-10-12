# -*- coding: utf-8 -*-

"""
Document Management System – Edit Document Module
"""

from typing import Dict

# Example in‑memory database. In a real system this would be replaced by persistent storage.
DOCUMENTS_DB: Dict[str, Dict[str, str]] = {
    "doc1": {"document_id": "doc1", "owner_id": "user123", "content": "Original content of doc1."},
    # Add more documents as needed.
}


def edit_document(
    member_id: str,
    member_role: str,
    doc_id: str,
    doc_owner_id: str,
    replacement_content: str
) -> str:
    """
    Update the content of an existing document if the user has sufficient permissions.

    Parameters
    ----------
    member_id : str
        The ID of the user attempting to modify the document.
    member_role : str
        The role of the user. Must be 'editor' to allow modifications.
    doc_id : str
        The unique identifier of the document to be edited.
    doc_owner_id : str
        The owner ID recorded for the document (should match the one in DOCUMENTS_DB).
    replacement_content : str
        The new content that will replace the current version.

    Returns
    -------
    str
        The updated document content.

    Raises
    ------
    PermissionError
        If the user does not have editor rights or is not the owner of the document.
    KeyError
        If the specified `doc_id` does not exist in DOCUMENTS_DB.

    Notes
    -----
    * This function performs a basic permission check. In production, consider more robust
      authentication/authorization mechanisms (e.g., JWT tokens, ACLs).
    * The function assumes that `doc_owner_id` is provided by the caller. In a real
      implementation, this value should be retrieved from the database to avoid tampering.
    """
    # Verify that the document exists
    if doc_id not in DOCUMENTS_DB:
        raise KeyError(f"Document with ID '{doc_id}' does not exist.")

    # Fetch the stored document data
    doc_record = DOCUMENTS_DB[doc_id]

    # Ensure that the provided owner ID matches the stored one (prevents tampering)
    if doc_owner_id != doc_record["owner_id"]:
        raise PermissionError("Provided owner ID does not match the document's actual owner.")

    # Check that the member has editing rights
    if member_role.lower() != "editor" or member_id != doc_owner_id:
        raise PermissionError("User does not have permission to edit this document.")

    # Perform the update
    doc_record["content"] = replacement_content

    return doc_record["content"]