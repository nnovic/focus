import threading
from abc import abstractmethod
from typing import Any


class DataSource:


    def start(self) -> None:
        self._stop_event = threading.Event()
        thread = threading.Thread(target=self._run, daemon=True)
        thread.start()

    def _run(self) -> None:
        try:
            self.connect()
            self.refresh()
            while not self._stop_event.is_set():
                self.poll()
                self._stop_event.wait(300)  # 5 minutes
        except Exception as e:
            breakpoint()
            raise
        finally:
            self.disconnect()

    def poll(self) -> None:
        pass

    def stop(self) -> None:
        self._stop_event.set()

    @abstractmethod
    def connect(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def disconnect(self) -> None:
        raise NotImplementedError()


    @abstractmethod
    def refresh(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def get_model(self, type_hint: str) -> Any:
        raise NotImplementedError()

    @abstractmethod
    def configure(self, config: Any):
        raise NotImplementedError()
