from abc import ABC, abstractmethod
import requests
from threading import Thread
from ..utils import exceptions

class BaseEventHandler(ABC):

    def start(self, *, update_interval = 0.1, thread=True):
        """
        Starts the cloud event handler.

        Keyword Arguments:
            update_interval (float): The clouddata log is continuosly checked for cloud updates. This argument provides the interval between these checks.
            thread (boolean): Whether the event handler should be run in a thread.
        """
        if self.running is False:
            self.update_interval = update_interval
            self.running = True
            if "on_ready" in self._events:
                self._events["on_ready"]()
            if thread:
                self._thread = Thread(target=self._update, args=())
                self._thread.start()
            else:
                self._thread = None
                self._update()

    @abstractmethod
    def _update(self):
        pass

    def stop(self):
        """
        Permanently stops the cloud event handler.
        """
        if self._thread is not None:
            self.running = False
            self._thread.join()
            self._thread = None

    def pause(self):
        """
        Pauses the cloud event handler.
        """
        self.running = False

    def resume(self):
        """
        Resumes the cloud event handler.
        """
        if self.running is False:
            self.start(update_interval=self.update_interval, thread=True)

    def event(self, function):
        """
        Decorator function. Adds a cloud event.
        """
        self._events[function.__name__] = function