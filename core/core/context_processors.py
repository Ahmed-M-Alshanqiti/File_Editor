from typing import Dict


def notifications_meta(request) -> Dict[str, int]:
    """
    Inject unread notification counts into every template.
    """
    if not request.user.is_authenticated:
        return {
            'notifications_unread_count': 0,
        }

    try:
        unread_count = request.user.notifications.filter(is_read=False).count()
    except Exception:
        unread_count = 0

    return {
        'notifications_unread_count': unread_count,
    }

