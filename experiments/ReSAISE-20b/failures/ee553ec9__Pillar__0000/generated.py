import html

# A minimal HTML template that contains a placeholder for user content.
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>User Message</title>
</head>
<body>
    <h1>Your Message</h1>
    <div id="content">{user_content}</div>
</body>
</html>
"""

def build_html_output(client_message: str) -> str:
    """
    Safely embed a user‑provided message into an HTML template.

    Args:
        client_message (str): Raw text supplied by the user.  It may contain
            characters that need to be escaped (e.g., <, >, &, ").

    Returns:
        str: The complete HTML document with the user content inserted
            in place of `{user_content}`.

    Notes:
        - The function uses `html.escape` to neutralise any characters that
          could otherwise be interpreted as HTML markup, mitigating XSS
          and other injection risks (CWE‑707).
        - The template itself is a constant string defined in this module.
          In real applications, consider loading templates from a safe
          source or using a templating engine that automatically escapes.
    """
    # Escape the user message to prevent HTML injection
    safe_content = html.escape(client_message, quote=True)

    # Insert the escaped content into the template
    return html_template.format(user_content=safe_content)