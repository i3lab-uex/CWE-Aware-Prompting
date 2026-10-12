# generate_xml_message.py

from xml.sax.saxutils import escape


def generate_xml_message(content_insert: str) -> str:
    """
    Build an XML message by safely inserting user supplied content into a
    predefined template. The function escapes special XML characters to
    prevent injection attacks (CWE‑74).

    Args:
        content_insert: Text supplied by the user that will be embedded
            inside the XML payload.

    Returns:
        A string containing the fully formed XML message.
    """
    # Predefined template with a placeholder for the user content
    xml_template = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<message>\n'
        '  <body>{content_insert}</body>\n'
        '</message>'
    )

    # Escape special XML characters in the user content
    safe_content = escape(content_insert, entities={"'": "&apos;", '"': "&quot;"})

    # Insert the escaped content into the template
    return xml_template.format(content_insert=safe_content)