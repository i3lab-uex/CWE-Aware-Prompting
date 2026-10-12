# -*- coding: utf-8 -*-
"""
Document modification helper for a corporate document management system.
"""

from typing import Dict

# Sample in-memory documents database
DOCUMENTS_DB: Dict[str, Dict[str, str]] = {
    # Example document structure:
    # "doc_123": {"document_id": "doc_123", "owner_id": "user_a", "content": "Initial content"},
}

def modify_document(
    user_id: str,
    role: str,
    doc_id: str,
    doc_owner: str,
    new_data: str
) -> str:
    """
    Update the content of a document if the user is authorized.

    Parameters
    ----------
    user_id : str
        ID of the user attempting to modify the document.
    role : str
        Role of the user ('viewer' or 'editor').
    doc_id : str
        Unique identifier for the document.
    doc_owner : str
        Owner ID of the document (should match DOCUMENTS_DB[doc_id]['owner_id']).
    new_data : str
        New content to replace the existing document content.

    Returns
    -------
    str
        The updated content of the document.

    Raises
    ------
    PermissionError
        If the user does not have permission to modify the document.
    KeyError
        If the specified document ID is not present in DOCUMENTS_DB.
    """
    # Verify that the document exists
    if doc_id not in DOCUMENTS_DB:
        raise KeyError(f"Document with ID '{doc_id}' does not exist.")

    # Retrieve the stored document record
    doc_record = DOCUMENTS_DB[doc_id]

    # Ensure that the provided doc_owner matches the stored owner
    if doc_record.get("owner_id") != doc_owner:
        raise ValueError("Provided document owner does not match the stored record.")

    # Authorization check: only editors who are also the owner can modify
    if role.lower() != "editor" or user_id != doc_owner:
        raise PermissionError("User is not authorized to modify this document.")

    # Perform the update
    doc_record["content"] = new_data

    return doc_record["content"]