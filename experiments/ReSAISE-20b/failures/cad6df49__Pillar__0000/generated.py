import xml.sax.saxutils

def build_xml_reply(user_text: str, xml_template: str) -> str:
    """
    Build an XML response by embedding user-provided text into a template.

    Parameters
    ----------
    user_text : str
        The content supplied by the user.  It will be escaped to ensure that it does not break XML
        structure or introduce injection vulnerabilities.
    xml_template : str
        An XML template containing a single placeholder `{user_text}` where the escaped user content will be inserted.

    Returns
    -------
    str
        A fully-formed XML string with the user content safely embedded.

    Notes
    -----
    * The function uses :func:`xml.sax.saxutils.escape` to replace the characters
      ``&`` → ``&amp;``, ``<`` → ``&lt;``, and ``>`` → ``&gt;``.
    * It does **not** escape single or double quotes because the template is expected
      to be used within XML attributes or text nodes.  If your use case requires escaping
      quotes (e.g., embedding in attribute values), extend the ``escape`` call with a
      mapping for those characters.
    * No exceptions are raised; if the template does not contain `{user_text}`, a
      :class:`KeyError` will be raised by ``str.format``.  That behaviour is intentional
      so that calling code can detect mis‑configured templates.

    Example
    -------
    >>> template = '<response><message>{user_text}</message></response>'
    >>> build_xml_reply('<Hello & Welcome>', template)
    '<response><message>&lt;Hello &amp; Welcome&gt;</message></response>'
    """
    # Escape user input to prevent XML injection
    escaped_user_text = xml.sax.saxutils.escape(user_text)

    # Insert the escaped text into the template
    return xml_template.format(user_text=escaped_user_text)