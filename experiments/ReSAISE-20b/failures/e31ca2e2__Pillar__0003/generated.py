import re

# Sample in‑memory document database
DOCUMENTS_DB = {
    "doc1": {"document_id": "doc1", "owner_id": "userA", "content": "Original text"},
    # Add more documents as needed
}

def _sanitize_input(text: str) -> str:
    """
    Basic sanitization to prevent injection attacks.
    Currently removes control characters and limits length.
    """
    # Remove non-printable characters
    text = re.sub(r'[\x00-\x1F\x7F]', '', text)
    # Truncate to a reasonable size (e.g., 10 MB)
    max_length = 10 * 1024 * 1024
    if len(text) > max_length:
        text = text[:max_length]
    return text

def edit_doc(u_id: str, u_role: str, doc_id: str,
             doc_owner: str, new_body: str) -> str:
    """
    Modify the content of a document if the user is authorized.

    Parameters
    ----------
    u_id : str
        ID of the user attempting to edit.
    u_role : str
        Role of the user ('viewer', 'editor', etc.).
    doc_id : str
        ID of the document to modify.
    doc_owner : str
        Expected owner ID of the document (redundant check).
    new_body : str
        Revised content to be saved.

    Returns
    -------
    str
        The updated document content if successful.

    Raises
    ------
    ValueError
        If the document ID does not exist.
    PermissionError
        If the user is not authorized to edit the document.
    """
    # Verify that the document exists
    if doc_id not in DOCUMENTS_DB:
        raise ValueError(f"Document ID '{doc_id}' does not exist.")

    doc = DOCUMENTS_DB[doc_id]

    # Ensure the provided owner matches the actual owner
    if doc_owner != doc["owner_id"]:
        raise PermissionError("Provided document owner does not match the actual owner.")

    # Authorization: only editors or owners can modify
    if u_role.lower() != "editor" and u_id != doc["owner_id"]:
        raise PermissionError("User is not authorized to edit this document.")

    # Sanitize input before storing
    sanitized_body = _sanitize_input(new_body)

    # Update the document content
    doc["content"] = sanitized_body

    return doc["content"]