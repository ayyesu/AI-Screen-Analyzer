import pyttsx3
from threading import Lock

class SpeechService:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(SpeechService, cls).__new__(cls)
                cls._instance._initialize()
            return cls._instance

    def _initialize(self):
        """Initialize the speech engine."""
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)  # Speed of speech
        self.engine.setProperty('volume', 1.0)  # Volume level
        self.is_speaking = False

    def speak(self, text):
        """Convert text to speech."""
        if not text:
            return

        self.stop()  # Stop any ongoing speech
        self.is_speaking = True
        self.engine.say(text)
        self.engine.runAndWait()
        self.is_speaking = False

    def stop(self):
        """Stop the current speech."""
        if self.is_speaking:
            self.engine.stop()
            self.is_speaking = False

    def set_rate(self, rate):
        """Set the speech rate (words per minute)."""
        self.engine.setProperty('rate', rate)

    def set_volume(self, volume):
        """Set the speech volume (0.0 to 1.0)."""
        self.engine.setProperty('volume', max(0.0, min(1.0, volume)))
