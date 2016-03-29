class NoImage(Exception):
    """
    Represents a container settings without image
    """
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class StatusError(Exception):
    """
    Exchange docker errors into nap errors
    """
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg
