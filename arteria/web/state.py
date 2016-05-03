
from arteria.exceptions import InvalidArteriaStateException

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

valid_states = set([State.NONE, State.PENDING, State.READY, State.STARTED, State.DONE, State.ERROR, State.CANCELLED])

def validate_state(state):
    """
    Raises InvalidRunfolderState if the state is not known
    :param state: to check
    :return: True if the state is valid
    :raises: InvalidArteriaStateException if the state is no valid
    """
    if state not in valid_states:
        raise InvalidArteriaStateException("The state '{}' is not valid".format(state))
    return True
