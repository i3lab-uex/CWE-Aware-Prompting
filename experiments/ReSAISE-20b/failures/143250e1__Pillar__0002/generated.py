# SPDX-License-Identifier: MIT

"""
Document modification module.

This module contains the `alter_document` function which enforces
proper access control when updating a document in a corporate
document management system. The function ensures that only users
with the 'editor' role or the original document owner can modify
the content. Any unauthorized attempt raises a PermissionError.

CWE-284: Improper Access Control
"""

from typing import Dict

# Simulated in‑memory database of documents.
DOCUMENTS_DB: Dict[str, Dict[str, str]] = {
    "doc-001": {"document_id": "doc-001", "owner_id": "user-123", "content": "Initial content A."},
    "doc-002": {"document_id": "doc-002", "owner_id": "user-456", "content": "Initial content B."},
    # Add more documents as needed.
}


def alter_document(
    modifier_id: str,
    user_role: str,
    doc_identifier: str,
    creator_id: str,
    updated_content: str,
) -> str:
    """
    Update the content of a document after performing access control checks.

    Parameters
    ----------
    modifier_id : str
        The ID of the user attempting to modify the document.
    user_role : str
        The role of the user ('viewer' or 'editor').
    doc_identifier : str
        The unique identifier of the document to modify.
    creator_id : str
        The ID of the original document owner. (Redundant check for safety.)
    updated_content : str
        The new content that will replace the existing document content.

    Returns
    -------
    str
        The updated content of the document.

    Raises
    ------
    PermissionError
        If the user does not have permission to modify the document.
    KeyError
        If the specified document identifier is not found in the database.
    ValueError
        If any of the required arguments are missing or invalid.

    Notes
    -----
    * The function performs a strict role and ownership check:
      - Only users with the 'editor' role can modify documents.
      - The document owner is also granted modification rights,
        regardless of the `user_role` value.
    * The `creator_id` argument is cross‑checked against the stored
      owner to guard against tampering.
    * All string comparisons are performed in a case‑sensitive manner
      to avoid accidental privilege escalation.
    """
    # Validate input arguments
    if not all(isinstance(arg, str) and arg for arg in [modifier_id, user_role, doc_identifier, creator_id]):
        raise ValueError("All identifiers must be non‑empty strings.")

    # Retrieve the document from the database
    try:
        doc = DOCUMENTS_DB[doc_identifier]
    except KeyError as exc:
        raise KeyError(f"Document with ID '{doc_identifier}' not found.") from exc

    # Cross‑check creator_id against stored owner_id
    if doc["owner_id"] != creator_id:
        raise ValueError("Provided creator_id does not match the document's owner.")

    # Access control: allow if user is editor or owner
    has_permission = (user_role == "editor") or (modifier_id == doc["owner_id"])
    if not has_permission:
        raise PermissionError("User does not have permission to modify this document.")

    # Perform the update
    doc["content"] = updated_content

    return doc["content"]