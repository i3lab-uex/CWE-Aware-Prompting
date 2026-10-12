import typing

# Example in‑memory database; in a real system this would be replaced by persistent storage.
DOCUMENTS_DB: dict[str, dict[str, typing.Any]] = {
    # Example entry:
    # "doc123": {"document_id": "doc123", "owner_id": "userA", "content": "Initial content."}
}


def revise_document(
    owner: str,
    editor_role: str,
    doc_ref: str,
    doc_creator: str,
    revised_content: str
) -> str:
    """
    Update the content of a document if the caller has sufficient permissions.

    Parameters
    ----------
    owner : str
        The ID of the user attempting to modify the document.
    editor_role : str
        Role of the caller; expected values are 'viewer' or 'editor'.
    doc_ref : str
        Unique identifier of the target document.
    doc_creator : str
        The ID of the user who originally created the document.
    revised_content : str
        New content to replace the existing one.

    Returns
    -------
    str
        The updated document content.

    Raises
    ------
    PermissionError
        If the caller is not authorized to modify the document.
    KeyError
        If the specified document does not exist in the database.
    """
    # Verify that the document exists
    if doc_ref not in DOCUMENTS_DB:
        raise KeyError(f"Document '{doc_ref}' does not exist.")

    doc = DOCUMENTS_DB[doc_ref]

    # Validate that the provided creator matches the stored owner
    if doc_creator != doc["owner_id"]:
        raise ValueError("Provided creator ID does not match the document's actual owner.")

    # Authorization logic:
    # - The original owner can always edit.
    # - Users with the 'editor' role are allowed to edit any document
    #   (subject to additional business rules in a real system).
    authorized = False

    if owner == doc["owner_id"]:
        authorized = True
    elif editor_role.lower() == "editor":
        authorized = True

    if not authorized:
        raise PermissionError("You do not have permission to modify this document.")

    # Perform the update
    doc["content"] = revised_content

    return doc["content"]