import xml.sax.saxutils

def build_xml_reply(user_text: str, xml_template: str) -> str:
    """
    Build a well‑formed XML response by inserting the user supplied text
    into ``xml_template``.  The function performs proper XML escaping to
    avoid injection or malformed documents (CWE‑707).

    Parameters
    ----------
    user_text : str
        Text supplied by the caller that must be embedded safely into XML.
    xml_template : str
        A string containing a single placeholder ``{user_text}`` where the
        escaped user content should be inserted.

    Returns
    -------
    str
        A fully‑formed XML string with the escaped user content inserted.
    """
    # Ensure the placeholder exists
    if "{user_text}" not in xml_template:
        raise ValueError("The XML template must contain a '{user_text}' placeholder")

    # Escape characters that have special meaning in XML
    escaped_user_text = xml.sax.saxutils.escape(
        user_text,
        entities={"'": "&apos;", '"': "&quot;"}  # also escape quotes
    )

    # Perform the substitution
    return xml_template.replace("{user_text}", escaped_user_text)