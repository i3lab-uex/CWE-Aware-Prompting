# -*- coding: utf-8 -*-
"""
A simple in‑memory document management helper.
"""

from __future__ import annotations
import logging

# Configure a basic logger for debugging / audit purposes.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

# Example in‑memory document store.
DOCUMENTS_DB: dict[str, dict[str, str]] = {
    # Example entry:
    # "doc_001": {"document_id": "doc_001", "owner_id": "user_a", "content": "Initial text."}
}

def alter_document(
    operator_id: str,
    operator_role: str,
    doc_id: str,
    doc_owner_id: str,
    updated_content: str,
) -> str:
    """
    Update the content of an existing document.

    Parameters
    ----------
    operator_id : str
        The ID of the user attempting to modify the document.
    operator_role : str
        Role of the user: either 'viewer' or 'editor'.
    doc_id : str
        The unique identifier of the target document.
    doc_owner_id : str
        The owner ID stored in the database for the document. (Used to validate ownership)
    updated_content : str
        The new content that will replace the current version.

    Returns
    -------
    str
        The updated document content upon successful modification.

    Raises
    ------
    PermissionError
        If the operator does not have permission to edit.
    KeyError
        If the document ID is not present in ``DOCUMENTS_DB``.
    ValueError
        If an unsupported role is supplied.
    """
    # Validate role
    if operator_role not in {"viewer", "editor"}:
        logging.error("Unsupported role: %s", operator_role)
        raise ValueError(f"Unsupported role: {operator_role}")

    # Document must exist
    if doc_id not in DOCUMENTS_DB:
        logging.error("Document ID '%s' not found.", doc_id)
        raise KeyError(f"Document ID '{doc_id}' does not exist.")

    document = DOCUMENTS_DB[doc_id]

    # Ensure the provided owner ID matches the database record
    if document["owner_id"] != doc_owner_id:
        logging.warning(
            "Owner ID mismatch for doc '%s': provided='%s', stored='%s'",
            doc_id,
            doc_owner_id,
            document["owner_id"],
        )
        raise PermissionError("Owner ID mismatch.")

    # Only editors may modify the document
    if operator_role != "editor":
        logging.warning(
            "User '%s' with role '%s' attempted to modify document '%s'.",
            operator_id,
            operator_role,
            doc_id,
        )
        raise PermissionError("Insufficient permissions to edit the document.")

    # Optional: Verify that the operator is the owner (or implement an admin flag)
    if operator_id != document["owner_id"]:
        logging.warning(
            "User '%s' is not the owner of document '%s'.",
            operator_id,
            doc_id,
        )
        raise PermissionError("Only the document owner can edit this document.")

    # Perform the update
    logging.info(
        "User '%s' is updating document '%s'.", operator_id, doc_id
    )
    document["content"] = updated_content

    # Return the new content for confirmation
    return document["content"]