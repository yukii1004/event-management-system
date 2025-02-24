from collections import defaultdict, deque


class EventWaitingList:
    # singleton class
    _instance = None

    def __new__(cls, *args, **kwargs):
        if EventWaitingList._instance is None:
            EventWaitingList._instance = object.__new__(cls)
            EventWaitingList._instance.__init__(*args, **kwargs)
        return EventWaitingList._instance

    def __init__(self, *args, **kwargs):
        self.waiting = defaultdict(lambda: deque())
