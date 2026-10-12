import html

# Example profile format template with placeholders.
PROFILE_FORMAT = """
<div class="user-profile">
    <h2>{full_name}</h2>
    <p class="about-me">{about_me}</p>
    <div class="status-update">
        <strong>Status:</strong> {status_update}
    </div>
</div>
"""

def generate_user_profile(full_name: str, about_me: str, status_update: str) -> str:
    """
    Construct a sanitized user profile HTML snippet.

    Parameters
    ----------
    full_name : str
        The user's self-provided name.
    about_me : str
        A user-authored biography that may contain multiple sentences.
    status_update : str
        A short, current status update submitted by the user.

    Returns
    -------
    str
        An HTML string ready for safe web display. All user-supplied content is
        escaped to prevent XSS (CWE‑79).
    """
    # Escape all user-supplied data to neutralize potential XSS payloads.
    safe_full_name = html.escape(full_name, quote=True)
    safe_about_me = html.escape(about_me, quote=True)
    safe_status_update = html.escape(status_update, quote=True)

    # Populate the template with sanitized values.
    profile_html = PROFILE_FORMAT.format(
        full_name=safe_full_name,
        about_me=safe_about_me,
        status_update=safe_status_update
    )
    return profile_html.strip()