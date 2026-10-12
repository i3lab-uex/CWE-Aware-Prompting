# -*- coding: utf-8 -*-
"""
Document modification module for a company document management system.
"""

from typing import Dict

# Example in-memory database of documents
DOCUMENTS_DB: Dict[str, Dict[str, str]] = {
    # "doc_id": {"document_id": str, "owner_id": str, "content": str}
    # Example entries can be added here
}


def modify_document(
    requester_id: str,
    requester_role: str,
    document_identifier: str,
    document_owner_id: str,
    modified_content: str,
) -> str:
    """
    Modify the content of an existing document.

    Parameters
    ----------
    requester_id : str
        ID of the user attempting to modify the document.
    requester_role : str
        Role of the user ('viewer' or 'editor').
    document_identifier : str
        Unique ID of the target document.
    document_owner_id : str
        Expected owner ID of the document (used for double‑check).
    modified_content : str
        New content to replace the current document content.

    Returns
    -------
    str
        The updated content of the document.

    Raises
    ------
    KeyError
        If the document does not exist in `DOCUMENTS_DB`.
    PermissionError
        If the requester is not authorized to modify the document.
    ValueError
        If `requester_role` is neither 'viewer' nor 'editor'.
    """
    # Validate role
    if requester_role not in {"viewer", "editor"}:
        raise ValueError(f"Invalid role '{requester_role}'. Must be 'viewer' or 'editor'.")

    # Retrieve the document
    try:
        doc = DOCUMENTS_DB[document_identifier]
    except KeyError as exc:
        raise KeyError(f"Document with ID '{document_identifier}' not found.") from exc

    # Verify that the owner_id in DB matches the supplied document_owner_id
    if doc.get("owner_id") != document_owner_id:
        raise ValueError(
            f"Owner ID mismatch for document '{document_identifier}'. "
            "Provided owner_id does not match database record."
        )

    # Authorization check: only editors can modify documents
    if requester_role != "editor":
        raise PermissionError(
            f"User '{requester_id}' with role '{requester_role}' "
            "is not authorized to modify documents."
        )

    # Ensure the requester is the owner
    if doc.get("owner_id") != requester_id:
        raise PermissionError(
            f"User '{requester_id}' is not the owner of document "
            f"'{document_identifier}'. Only the owner may modify it."
        )

    # All checks passed – perform the update
    doc["content"] = modified_content

    return doc["content"]