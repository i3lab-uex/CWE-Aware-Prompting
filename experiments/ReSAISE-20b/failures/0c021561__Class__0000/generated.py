from __future__ import annotations

import typing as _t

# Example in‑memory document store
DOCUMENTS_DB: dict[str, dict[str, _t.Any]] = {
    # Example entry:
    # "doc1": {"document_id": "doc1", "owner_id": "user123", "content": "Original text."}
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
        Role of the user (e.g., 'viewer', 'editor').
    docu_id : str
        ID of the target document.
    creator_id : str
        ID of the original document creator (owner).
    updated_definition : str
        New content to replace the existing one.

    Returns
    -------
    str
        The updated document content.

    Raises
    ------
    PermissionError
        If the user does not have edit permissions.
    KeyError
        If the document ID is not found in `DOCUMENTS_DB`.
    """
    # Ensure required arguments are of correct type
    if not all(isinstance(arg, str) for arg in (usr_id, usr_role, docu_id, creator_id, updated_definition)):
        raise TypeError("All arguments must be strings.")

    # Verify that the document exists
    if docu_id not in DOCUMENTS_DB:
        raise KeyError(f"Document ID '{docu_id}' does not exist.")

    # Authorization check: user must be an editor and either the creator or owner
    if usr_role.lower() != "editor" or usr_id not in {creator_id, DOCUMENTS_DB[docu_id]["owner_id"]}:
        raise PermissionError("User is not authorized to modify this document.")

    # Perform the update
    DOCUMENTS_DB[docu_id]["content"] = updated_definition

    # Return the new content
    return DOCUMENTS_DB[docu_id]["content"]