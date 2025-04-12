import threading
import time
import keyboard

class HotkeyManager:
    def __init__(self, config_manager):
        self.config_manager = config_manager
        self.running = True
        self.hotkey_thread = None
        self.callback = None

    def start_listening(self, callback):
        self.callback = callback
        self.hotkey_thread = threading.Thread(target=self.listen_for_hotkey)
        self.hotkey_thread.daemon = True
        self.hotkey_thread.start()

    def listen_for_hotkey(self):
        hotkey = self.config_manager.get('API', 'hotkey')
        keyboard.add_hotkey(hotkey, self.callback)

        while self.running:
            time.sleep(0.1)

    def stop_listening(self):
        self.running = False
        if self.hotkey_thread and self.hotkey_thread.is_alive():
            self.hotkey_thread.join(timeout=1.0)
