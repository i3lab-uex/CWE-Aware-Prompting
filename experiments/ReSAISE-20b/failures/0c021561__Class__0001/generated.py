# -*- coding: utf-8 -*-
"""
Document management helper – revise document content.

The function verifies that the requesting user has the right to modify a
document.  Only an `editor` or the document owner can perform updates.
Unauthorized attempts raise a PermissionError.

CWE-863 (Incorrect Authorization) is mitigated by performing a strict
role/ownership check before any modification.
"""

from __future__ import annotations

# Example in-memory document store
DOCUMENTS_DB: dict[str, dict] = {
    "doc1": {"document_id": "doc1", "owner_id": "user123", "content": "Initial text."},
    # Add more documents as needed
}

def revise_doc(
    usr_id: str,
    usr_role: str,
    docu_id: str,
    creator_id: str,
    updated_definition: str,
) -> str:
    """
    Update the content of a document if the user is authorized.

    Parameters
    ----------
    usr_id : str
        ID of the user attempting to modify the document.
    usr_role : str
        Role of the user ('viewer', 'editor', etc.).
    docu_id : str
        ID of the target document.
    creator_id : str
        ID of the document's creator (owner).
    updated_definition : str
        New content to be stored.

    Returns
    -------
    str
        The updated document content.

    Raises
    ------
    KeyError
        If the specified document does not exist in `DOCUMENTS_DB`.
    PermissionError
        If the user is not authorized to modify the document.
    """
    # Ensure the document exists
    if docu_id not in DOCUMENTS_DB:
        raise KeyError(f"Document '{docu_id}' not found.")

    # Authorization check: only editors or the owner can modify
    if usr_role.lower() != "editor" and usr_id != creator_id:
        raise PermissionError(
            f"User '{usr_id}' with role '{usr_role}' is not authorized to modify document '{docu_id}'."
        )

    # Perform the update
    DOCUMENTS_DB[docu_id]["content"] = updated_definition

    # Return the new content
    return DOCUMENTS_DB[docu_id]["content"]


# Example usage (for testing purposes only)
if __name__ == "__main__":
    try:
        new_content = revise_doc(
            usr_id="user123",
            usr_role="editor",
            docu_id="doc1",
            creator_id="user123",
            updated_definition="Updated text by owner.",
        )
        print("Document updated successfully:", new_content)
    except Exception as e:
        print(f"Error: {e}")