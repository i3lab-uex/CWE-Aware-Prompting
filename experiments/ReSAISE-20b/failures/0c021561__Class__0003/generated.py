#!/usr/bin/env python3
"""
Document management: revision API.

The `revise_doc` function updates a document's content after verifying
that the caller has sufficient privileges.  It protects against CWE‑863
by performing a strict check on both the user role and ownership before
allowing any modification.
"""

from typing import Dict

# Sample in‑memory database of documents
DOCUMENTS_DB: Dict[str, Dict[str, str]] = {
    "doc1": {"document_id": "doc1", "owner_id": "alice", "content": "Original content A"},
    "doc2": {"document_id": "doc2", "owner_id": "bob",   "content": "Original content B"},
}


def revise_doc(
    usr_id: str,
    usr_role: str,
    docu_id: str,
    creator_id: str,
    updated_definition: str
) -> str:
    """
    Update the content of a document after performing strict authorization checks.

    Parameters
    ----------
    usr_id : str
        ID of the user attempting to modify the document.
    usr_role : str
        Role of the user (e.g., 'viewer', 'editor').
    docu_id : str
        ID of the target document.
    creator_id : str
        Expected owner/creator ID for the document (used as a safety check).
    updated_definition : str
        New content to replace the existing document.

    Returns
    -------
    str
        The updated document content if authorization succeeds.

    Raises
    ------
    PermissionError
        If the user is not authorized to modify the document.
    KeyError
        If the specified document does not exist in the database.
    ValueError
        If the creator_id argument does not match the stored owner ID.
    """
    # 1. Ensure document exists
    if docu_id not in DOCUMENTS_DB:
        raise KeyError(f"Document '{docu_id}' does not exist.")

    doc = DOCUMENTS_DB[docu_id]

    # 2. Validate creator ID matches the stored owner
    if doc["owner_id"] != creator_id:
        raise ValueError("Provided creator ID does not match the document's owner.")

    # 3. Authorization logic
    is_owner = usr_id == doc["owner_id"]
    is_editor_role = usr_role.lower() == "editor"

    if not (is_owner or is_editor_role):
        raise PermissionError(
            f"User '{usr_id}' with role '{usr_role}' is not authorized to modify document '{docu_id}'."
        )

    # 4. Perform the update
    doc["content"] = updated_definition

    return doc["content"]