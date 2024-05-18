from abc import abstractmethod


class Scrollable:
    @abstractmethod

    def check_scroll(self, scroll):
        pass
class Observable:
    def __init__(self):
        self.observers = []

    def add_observer(self, observer):
        pass

    def remove_observer(self):
        pass

    def notify_observers(self):
        pass


class TextObservable(Observable):

    def __init__(self):
        super().__init__()
        self.observers = []

    pass
