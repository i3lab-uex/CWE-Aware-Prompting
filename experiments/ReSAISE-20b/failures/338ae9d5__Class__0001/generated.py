import xml.sax.saxutils

def create_xml_output(input_content: str) -> str:
    """
    Create an XML response by inserting the user supplied content into a
    pre-defined template.  The input is escaped to prevent XML injection
    (CWE‑74).

    Parameters
    ----------
    input_content : str
        The text supplied by the user to be inserted into the XML structure.

    Returns
    -------
    str
        The constructed XML response that integrates the escaped input.
    """
    xml_template = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<response>\n'
        '    <content>{input_content}</content>\n'
        '</response>'
    )

    # Escape special XML characters to avoid injection.
    safe_content = xml.sax.saxutils.escape(input_content, entities={"'": "&apos;", '"': "&quot;"})

    return xml_template.format(input_content=safe_content)