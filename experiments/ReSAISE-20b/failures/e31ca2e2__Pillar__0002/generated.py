import typing

# Simulated document storage
DOCUMENTS_DB: dict[str, dict[str, str]] = {
    # Example entry:
    # "doc1": {"document_id": "doc1", "owner_id": "user123", "content": "Original content"}
}

def edit_doc(u_id: str, u_role: str, doc_id: str,
             doc_owner: str, new_body: str) -> typing.Union[str, None]:
    """
    Update the content of a document if the user is authorized.

    Parameters
    ----------
    u_id : str
        ID of the user attempting to edit.
    u_role : str
        Role of the user (e.g., 'viewer', 'editor').
    doc_id : str
        ID of the document to modify.
    doc_owner : str
        Expected owner ID of the document. (Optional for extra safety.)
    new_body : str
        New content to be stored.

    Returns
    -------
    str
        The updated content if authorization succeeds.
    None
        If the user is not authorized.

    Raises
    ------
    ValueError
        If `doc_id` does not exist in `DOCUMENTS_DB`.
    """
    # 1. Verify document exists
    doc = DOCUMENTS_DB.get(doc_id)
    if doc is None:
        raise ValueError(f"Document ID '{doc_id}' not found.")

    # 2. Double‑check ownership matches the provided doc_owner (optional safety)
    if doc["owner_id"] != doc_owner:
        # This could indicate tampering with the provided owner ID
        return None

    # 3. Authorization: allow if user is the owner or has 'editor' role
    if u_id == doc["owner_id"] or u_role.lower() == "editor":
        # 4. Perform the update
        doc["content"] = new_body
        return doc["content"]

    # 5. Unauthorized: return None (or you could raise a custom exception)
    return None