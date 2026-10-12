import xml.sax.saxutils as saxutils

# Predefined XML template with a placeholder for user content
xml_template = """<?xml version="1.0" encoding="UTF-8"?>
<response>
    <message>{user_entry}</message>
</response>"""

def produce_xml_message(user_entry: str) -> str:
    """
    Generate an XML response by inserting the user-provided entry into a
    predefined template. The function escapes special XML characters to
    prevent injection or malformed XML.

    Parameters:
        user_entry (str): The raw input from the user that will be embedded
                          in the XML structure.

    Returns:
        str: A well‑formed XML string containing the escaped user content.
    """
    # Escape characters that have special meaning in XML
    safe_entry = saxutils.escape(user_entry, entities={"'": "&apos;", '"': "&quot;"})
    # Insert the escaped entry into the template
    return xml_template.format(user_entry=safe_entry)