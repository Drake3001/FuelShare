import asyncio
import inspect
from PyQt6.QtCore import QThread, pyqtSignal


class BackgroundWorker(QThread):
    task_finished = pyqtSignal(str, object)
    task_error = pyqtSignal(str, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.loop = None

    def run(self):
        """Uruchamia pętlę asyncio w osobnym wątku."""
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()
        pending = asyncio.all_tasks(self.loop)
        for task in pending:
            task.cancel()
        self.loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
        self.loop.close()

    def submit(self, task_name: str, func, *args):
        if self.loop is None or not self.loop.is_running():
            self.task_error.emit(task_name, "Worker nie jest uruchomiony")
            return

        if inspect.iscoroutinefunction(func):
            # Przypadek ASYNC: tworzymy korutynę wywołując funkcję
            coro = func(*args)
            future = asyncio.run_coroutine_threadsafe(coro, self.loop)
        else:
            # Przypadek SYNC: odpalamy w executorze
            # run_in_executor zwraca obiekt Future, który jest kompatybilny
            future = self.loop.run_in_executor(None, func, *args)

        future.add_done_callback(
            lambda f: self._on_done(task_name, f)
        )

    def _on_done(self, task_name: str, future):
        try:
            result = future.result()
            self.task_finished.emit(task_name, result)
        except Exception as e:
            self.task_error.emit(task_name, str(e))

    def stop(self):
        if self.loop and self.loop.is_running():
            self.loop.call_soon_threadsafe(self.loop.stop)
        self.wait()
