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

class UpdateObservable:
    def __init__(self):
        self.update_observers = []

    def add_update_observer(self, observer):
        self.update_observers.append(observer)

    def remove_update_observer(self):
        pass

    def notify_update_observers(self):
        pass


class TextObservable(Observable):

    def __init__(self):
        super().__init__()
        self.observers = []

    pass
