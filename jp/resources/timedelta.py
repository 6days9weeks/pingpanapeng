from datetime import datetime


def format_time(start_time):
    fmt = start_time.strftime("%a, %b %d, %Y %X")
    days = round((datetime.utcnow() - start_time).total_seconds() / 86400)
    fmt += f"\n*{days} {'days' if days != 1 else 'day'} ago*"
    return fmt
