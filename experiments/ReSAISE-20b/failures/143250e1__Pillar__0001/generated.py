# -*- coding: utf-8 -*-
"""
Document modification helper for a corporate document management system.

The module defines the function `alter_document`, which updates a
document's content only if the caller has proper authorization.
"""

from typing import Dict

# Example in-memory database of documents.
DOCUMENTS_DB: Dict[str, Dict[str, str]] = {
    "doc_001": {"document_id": "doc_001", "owner_id": "user_a", "content": "Initial content A."},
    "doc_002": {"document_id": "doc_002", "owner_id": "user_b", "content": "Initial content B."},
    # Add more documents as needed.
}


def alter_document(
    modifier_id: str,
    user_role: str,
    doc_identifier: str,
    creator_id: str,
    updated_content: str
) -> str:
    """
    Update the content of a document if the modifier is authorized.

    Parameters
    ----------
    modifier_id : str
        The ID of the user attempting to modify the document.
    user_role : str
        Role of the user, expected values are 'viewer' or 'editor'.
    doc_identifier : str
        Unique identifier of the target document.
    creator_id : str
        The ID of the original owner/creator of the document.
    updated_content : str
        New content that will replace the existing document content.

    Returns
    -------
    str
        The updated content of the document upon successful modification.

    Raises
    ------
    PermissionError
        If the user does not have permission to modify the document.
    KeyError
        If the specified document identifier is not present in the database.

    Notes
    -----
    - Only users with the role 'editor' are permitted to modify documents.
      Viewers (or any other roles) are denied access regardless of ownership.
    - The function also verifies that the supplied `creator_id` matches
      the owner stored in the database to guard against tampering.
    - The implementation follows CWE-284 (Improper Access Control)
      guidelines by explicitly checking both role and ownership.
    """
    # Validate that the document exists
    if doc_identifier not in DOCUMENTS_DB:
        raise KeyError(f"Document '{doc_identifier}' does not exist.")

    doc_record = DOCUMENTS_DB[doc_identifier]

    # Ensure the creator_id matches the stored owner to prevent spoofing
    if doc_record["owner_id"] != creator_id:
        raise PermissionError("Creator ID mismatch; potential tampering detected.")

    # Enforce role-based access control
    if user_role.lower() != "editor":
        raise PermissionError("User role does not permit document modification.")

    # Optionally, enforce that only the owner can edit (commented out to allow any editor)
    # if modifier_id != doc_record["owner_id"]:
    #     raise PermissionError("Only the document owner can modify this content.")

    # Perform the update
    doc_record["content"] = updated_content

    return doc_record["content"]