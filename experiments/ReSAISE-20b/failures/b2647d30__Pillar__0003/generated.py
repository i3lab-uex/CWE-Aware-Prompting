# -*- coding: utf-8 -*-
"""
Document Management – Alter Document

This module provides a single function, `alter_document`, that safely updates
the content of an existing document in the `DOCUMENTS_DB`.  The function enforces
proper access control (CWE‑284) by ensuring that only users with the 'editor'
role and who are the owner of the document can modify it.  Unauthorized attempts
raise a `PermissionError`.

Author: ChatGPT
"""

from typing import Dict

# Sample in‑memory database.  In a real system this would be replaced by
# persistent storage such as a relational database or an object store.
DOCUMENTS_DB: Dict[str, Dict[str, str]] = {
    "doc1": {"document_id": "doc1", "owner_id": "user123", "content": "Initial content"},
    # ... additional documents ...
}


def alter_document(
    operator_id: str,
    operator_role: str,
    doc_id: str,
    doc_owner_id: str,
    updated_content: str
) -> str:
    """
    Update the content of an existing document.

    Parameters
    ----------
    operator_id : str
        ID of the user attempting the modification.
    operator_role : str
        Role of the user; must be 'editor' to modify documents.
    doc_id : str
        Unique identifier of the target document.
    doc_owner_id : str
        Owner ID stored in the document; used for an extra consistency check.
    updated_content : str
        New content that will replace the current document body.

    Returns
    -------
    str
        The updated content of the document.

    Raises
    ------
    PermissionError
        If the operator does not have sufficient permissions or the
        provided owner ID does not match the stored value.
    KeyError
        If the document with `doc_id` does not exist in the database.

    Notes
    -----
    - The function performs a strict equality check on `operator_role`
      and `operator_id` against the stored owner to mitigate
      improper access control.
    - The database is accessed directly for simplicity; in a production
      environment use proper isolation and locking mechanisms.
    """
    # 1. Verify that the document exists
    if doc_id not in DOCUMENTS_DB:
        raise KeyError(f"Document with ID '{doc_id}' does not exist.")

    # 2. Retrieve the stored document record
    doc_record = DOCUMENTS_DB[doc_id]

    # 3. Ensure the provided owner ID matches the stored one
    if doc_owner_id != doc_record["owner_id"]:
        raise PermissionError("Provided owner ID does not match the document's owner.")

    # 4. Check that the operator has the 'editor' role and is the owner
    if not (operator_role == "editor" and operator_id == doc_owner_id):
        raise PermissionError("Insufficient permissions to modify this document.")

    # 5. Perform the update
    doc_record["content"] = updated_content

    return doc_record["content"]


# Example usage (for testing purposes)
if __name__ == "__main__":
    try:
        new_content = alter_document(
            operator_id="user123",
            operator_role="editor",
            doc_id="doc1",
            doc_owner_id="user123",
            updated_content="Updated content goes here."
        )
        print(f"Document updated successfully: {new_content}")
    except Exception as e:
        print(f"Error: {e}")