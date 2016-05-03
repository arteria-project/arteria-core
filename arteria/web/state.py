
"""
Status conventions to be returned by arteria services
when running jobs and querying for their status.
"""
class State:
    NONE = "none"
    PENDING = "pending"
    READY = "ready"
    STARTED = "started"
    DONE = "done"
    ERROR = "error"
    CANCELLED = "cancelled"

