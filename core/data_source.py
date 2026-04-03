import threading
from abc import abstractmethod
from typing import Any


class DataSource:

    def __init__(self) -> None:
        self.__refresh_callbacks = []
        self._stop_event = threading.Event()
        self.__connected = False

    def start(self) -> None:
        thread = threading.Thread(target=self.__source_task, daemon=True)
        thread.start()

    def __source_task(self) -> None:

        try:
            self.connect()
            self.__stay_connected_loop()
        except Exception as e:
            breakpoint()
            raise
        finally:
            self.disconnect()

    def __stay_connected_loop(self) -> None:
        while not self._stop_event.is_set():
            try:
                if not self.__connected:
                    self.connect()
                self.__connected_loop()
            except ConnectionError as e:
                self.disconnect()

    def __connected_loop(self) -> None:
        try:
            self.refresh()
            while not self._stop_event.is_set():
                self._stop_event.wait(120)  # 2 minutes
                self.poll()
        except Exception as e:
            raise

    @property
    def is_connected(self) -> bool:
        return self.__connected

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

    def connect(self) -> None:
        self._connect()
        self.__connected = True

    @abstractmethod
    def _connect(self) -> None:
        raise NotImplementedError()

    def disconnect(self) -> None:
        try:
            self._disconnect()
        finally:
            self.__connected = False

    @abstractmethod
    def _disconnect(self) -> None:
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

    def _prompt_user_for(self, credentials: dict):
        pass
