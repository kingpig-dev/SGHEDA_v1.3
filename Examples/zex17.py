from plyer import notification

def show_error_notification(error_message):
    notification.notify(
        title="Error",
        message=error_message,
        app_icon=None,  # You can specify a custom icon file path here
        timeout=10  # How long the notification should be displayed (in seconds)
    )

error_message = "File not found."
show_error_notification(error_message)