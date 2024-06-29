from ..utils.enums import ThreadState

thread_states = {}


def get_thread_state(thread_id):
    return thread_states.get(thread_id, ThreadState.AWAITING_LOGS)


def set_thread_state(thread_id, state):
    thread_states[thread_id] = state
