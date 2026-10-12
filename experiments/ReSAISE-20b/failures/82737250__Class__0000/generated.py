# -*- coding: utf-8 -*-

"""
A simple in‑memory document management module.
"""

from typing import Dict

# Example in‑memory database. In production this would be replaced
# by a persistent store (e.g., SQL, NoSQL) with proper access controls.
DOCUMENTS_DB: Dict[str, Dict[str, str]] = {
    "doc1": {"document_id": "doc1", "owner_id": "user123", "content": "Original content of doc1."},
    "doc2": {"document_id": "doc2", "owner_id": "user456", "content": "Original content of doc2."},
}


def modify_document(
    requester_id: str,
    requester_role: str,
    document_identifier: str,
    document_owner_id: str,
    modified_content: str,
) -> str:
    """
    Update the content of an existing document.

    Parameters
    ----------
    requester_id : str
        ID of the user attempting to modify the document.
    requester_role : str
        Role of the requester; must be 'editor' to modify documents.
    document_identifier : str
        Unique identifier of the target document.
    document_owner_id : str
        Owner ID stored in the document (used for consistency check).
    modified_content : str
        New content to replace the current version.

    Returns
    -------
    str
        The updated document content.

    Raises
    ------
    KeyError
        If the requested document does not exist in ``DOCUMENTS_DB``.
    PermissionError
        If the requester is not an editor or if the owner ID does not match.
    ValueError
        If any required argument is missing or invalid.
    """

    # Basic input validation
    if not all([requester_id, requester_role, document_identifier, modified_content]):
        raise ValueError("All arguments except `document_owner_id` must be provided and non-empty.")

    # Ensure the requester role is valid
    if requester_role not in {"viewer", "editor"}:
        raise ValueError("requester_role must be either 'viewer' or 'editor'.")

    # Retrieve the document
    try:
        doc = DOCUMENTS_DB[document_identifier]
    except KeyError as exc:
        raise KeyError(f"Document with ID '{document_identifier}' not found.") from exc

    # Verify that the owner_id in the document matches the supplied one
    if doc["owner_id"] != document_owner_id:
        raise PermissionError("Provided owner ID does not match the document's actual owner.")

    # Authorization check: only editors can modify
    if requester_role != "editor":
        raise PermissionError("User does not have permission to modify documents.")

    # Perform the update
    doc["content"] = modified_content

    return doc["content"]