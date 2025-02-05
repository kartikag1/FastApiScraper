class Notifier:
    def __init__(self, recipients=None):
        self.recipients = recipients or ["admin@example.com"]

    def notify(self, message):
        """Notify recipients (print to console for now)."""
        print(f"Notification: {message}")
        # Here other notification svc can be added - email etc
        for recipient in self.recipients:
            print(f"Sending to {recipient}: {message}")
