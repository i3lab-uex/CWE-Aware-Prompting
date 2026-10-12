# -*- coding: utf-8 -*-

"""
Document Management – Revision Service

This module provides the `revise_doc` function which allows authorized users to
update the content of a document stored in an in‑memory database.
"""

from typing import Dict

# Sample in‑memory document store
DOCUMENTS_DB: Dict[str, dict] = {
    # Example entry:
    # "doc_001": {"document_id": "doc_001", "owner_id": "user_a", "content": "Original text"}
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
        ID of the user attempting to modify the document.
    usr_role : str
        Role of the user (e.g., 'viewer', 'editor').
    docu_id : str
        ID of the document to be updated.
    creator_id : str
        ID of the original creator of the document.
    updated_definition : str
        New content to replace the existing document text.

    Returns
    -------
    str
        The updated content of the document.

    Raises
    ------
    PermissionError
        If the user does not have permission to modify the document.
    KeyError
        If the document ID is not found in `DOCUMENTS_DB`.
    """
    # Ensure the document exists
    if docu_id not in DOCUMENTS_DB:
        raise KeyError(f"Document ID '{docu_id}' does not exist.")

    doc = DOCUMENTS_DB[docu_id]

    # Authorization logic:
    # 1. The user must be the creator (owner) of the document, or
    # 2. The user must have an 'editor' role.
    is_owner = (doc.get("owner_id") == usr_id)
    is_editor_role = (usr_role.lower() == "editor")

    if not (is_owner or is_editor_role):
        raise PermissionError(
            f"User '{usr_id}' with role '{usr_role}' is not authorized to modify document '{docu_id}'."
        )

    # Perform the update
    doc["content"] = updated_definition

    # Optionally, store metadata like last modified by / timestamp here.

    return doc["content"]


# Example usage (for testing purposes only):
if __name__ == "__main__":
    # Populate a sample document
    DOCUMENTS_DB["doc_001"] = {
        "document_id": "doc_001",
        "owner_id": "user_a",
        "content": "Original content"
    }

    try:
        new_content = revise_doc(
            usr_id="user_a",
            usr_role="viewer",
            docu_id="doc_001",
            creator_id="user_a",
            updated_definition="Updated content by owner."
        )
        print("Success:", new_content)
    except PermissionError as e:
        print("Permission error:", e)

    try:
        # Editor role override
        new_content = revise_doc(
            usr_id="user_b",
            usr_role="editor",
            docu_id="doc_001",
            creator_id="user_a",
            updated_definition="Updated content by editor."
        )
        print("Success:", new_content)
    except PermissionError as e:
        print("Permission error:", e)

    try:
        # Unauthorized user
        revise_doc(
            usr_id="user_c",
            usr_role="viewer",
            docu_id="doc_001",
            creator_id="user_a",
            updated_definition="Attempt by unauthorized user."
        )
    except PermissionError as e:
        print("Permission error:", e)