import xml.sax.saxutils

def produce_xml_message(user_entry: str) -> str:
    """
    Return a fully‑formed XML string with the user entry safely embedded
    in the provided template.

    The function escapes characters that have special meaning in XML
    (e.g. <, >, &, ', ") to prevent injection attacks such as CWE‑74.

    Args:
        user_entry: The raw string supplied by the user.

    Returns:
        A string containing the XML document with the escaped user content.
    """
    # Predefined template with a placeholder for the user entry
    xml_template = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<response>\n'
        '  <user_input>{user_entry}</user_input>\n'
        '</response>'
    )

    # Escape user input to neutralize special XML characters
    safe_user_entry = xml.sax.saxutils.escape(user_entry, {"'": "&apos;", '"': "&quot;"})

    # Format the template with the escaped content
    return xml_template.format(user_entry=safe_user_entry)