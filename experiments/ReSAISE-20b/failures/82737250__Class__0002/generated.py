# -*- coding: utf-8 -*-
"""
A minimal in‑memory document management helper.
"""

from typing import Dict

# Sample in-memory database
DOCUMENTS_DB: Dict[str, Dict[str, str]] = {
    "doc1": {"document_id": "doc1", "owner_id": "user123", "content": "Original content"},
    # Add more documents as needed
}


def modify_document(
    requester_id: str,
    requester_role: str,
    document_identifier: str,
    document_owner_id: str,
    modified_content: str,
) -> str:
    """
    Update the content of a document if the requester is authorized.

    Parameters
    ----------
    requester_id : str
        ID of the user attempting the modification.
    requester_role : str
        Role of the user; must be 'editor' to modify documents.
    document_identifier : str
        Unique ID of the target document.
    document_owner_id : str
        Owner ID of the document (should match the database entry).
    modified_content : str
        New content that will replace the current document.

    Returns
    -------
    str
        The updated content of the document.

    Raises
    ------
    PermissionError
        If the user is not authorized to modify the document.
    KeyError
        If the document does not exist in the database.
    ValueError
        If role is invalid or mismatched owner ID.
    """
    # 1. Validate role
    if requester_role != "editor":
        raise PermissionError("Only users with 'editor' role may modify documents.")

    # 2. Retrieve document from DB
    try:
        doc = DOCUMENTS_DB[document_identifier]
    except KeyError as exc:
        raise KeyError(f"Document '{document_identifier}' not found.") from exc

    # 3. Verify owner ID matches database
    if doc["owner_id"] != document_owner_id:
        raise ValueError("Provided owner ID does not match the database record.")

    # 4. Authorization: allow modification if requester is owner or has editor role
    # Since we already checked role, just ensure the document exists.
    # (CWE-863: avoid mis‑authorizing by ensuring all checks are applied.)
    if requester_id != doc["owner_id"]:
        # In this simple system, only owners are allowed to edit.
        raise PermissionError("User is not the owner of the document.")

    # 5. Perform update
    doc["content"] = modified_content

    return doc["content"]