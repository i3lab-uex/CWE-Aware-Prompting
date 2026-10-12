# SPDX-License-Identifier: MIT

"""
Document revision module.

This module provides a single function, `revise_doc`, that safely updates the
content of a document in an in‑memory database.  Authorization checks are
performed to prevent unauthorized modifications (CWE-863).
"""

from typing import Dict

# Example in‑memory document database.
# In a real application this would be replaced by persistent storage or an
# external service.  Each document record contains:
#
#   - 'document_id': unique identifier of the document
#   - 'owner_id'    : user id of the creator / owner
#   - 'content'     : current document content (string)
DOCUMENTS_DB: Dict[str, Dict[str, str]] = {
    "doc1": {"document_id": "doc1", "owner_id": "userA", "content": "Initial content of doc1."},
    "doc2": {"document_id": "doc2", "owner_id": "userB", "content": "Initial content of doc2."},
    # ... add more documents as needed
}


def revise_doc(
    usr_id: str,
    usr_role: str,
    docu_id: str,
    creator_id: str,
    updated_definition: str
) -> str:
    """
    Update the content of a document if the user is authorized.

    Parameters
    ----------
    usr_id : str
        The ID of the user attempting to make the update.
    usr_role : str
        The role of the user (e.g., 'viewer', 'editor').
    docu_id : str
        The ID of the document to modify.
    creator_id : str
        The ID of the document's original creator.
    updated_definition : str
        The new content to be stored.

    Returns
    -------
    str
        The updated document content.

    Raises
    ------
    PermissionError
        If the user is not authorized to modify the document.
    KeyError
        If the requested document does not exist in `DOCUMENTS_DB`.
    """
    # Verify that the document exists.
    if docu_id not in DOCUMENTS_DB:
        raise KeyError(f"Document with id '{docu_id}' does not exist.")

    doc = DOCUMENTS_DB[docu_id]

    # Authorization logic:
    # - The user must be the document owner (creator) OR have an 'editor' role.
    # - The creator_id passed in must match the stored owner_id to avoid
    #   tampering via request parameters.
    is_owner = usr_id == doc["owner_id"] and creator_id == doc["owner_id"]
    is_editor = usr_role.lower() == "editor"

    if not (is_owner or is_editor):
        raise PermissionError(
            f"User '{usr_id}' with role '{usr_role}' is not authorized to modify document '{docu_id}'."
        )

    # Perform the update.
    doc["content"] = updated_definition

    return doc["content"]