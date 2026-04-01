import threading
from abc import abstractmethod
from typing import Any


class DataSource:

    def __init__(self) -> None:
        self.__refresh_callbacks = []
        self._stop_event = threading.Event()

    def start(self) -> None:
        thread = threading.Thread(target=self._run, daemon=True)
        thread.start()

    def _run(self) -> None:
        try:
            self.connect()
            self.refresh()
            while not self._stop_event.is_set():
                self._stop_event.wait(120)  # 5 minutes
                self.poll()
        except Exception as e:
            breakpoint()
            raise
        finally:
            self.disconnect()

    def poll(self) -> None:
        self.refresh()

    def stop(self) -> None:
        self._stop_event.set()

    def on_refresh(self, callback) -> None:
        self.__refresh_callbacks.append(callback)

    def __emit_refresh(self) -> None:
        for callback in self.__refresh_callbacks:
            try:
                callback()
            except Exception as e:
                breakpoint()
                raise

    @abstractmethod
    def connect(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def disconnect(self) -> None:
        raise NotImplementedError()


    def refresh(self) -> None:
        self._refresh()
        self.__emit_refresh()
    
    @abstractmethod
    def _refresh(self) -> None:
        raise NotImplementedError()
    
    @abstractmethod
    def get_model(self, type: type) -> Any:
        raise NotImplementedError()

    @abstractmethod
    def configure(self, config: Any):
        raise NotImplementedError()
