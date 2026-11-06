import os, json, threading
from pathlib import Path
import requests
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from plyer import filechooser

BASE = Path(os.environ.get("ANDROID_PRIVATE", str(Path.home()))) / "monu_voice_editor"
BASE.mkdir(parents=True, exist_ok=True)
CONFIG = BASE / "settings.json"

KV = r"""
<Root>:
    orientation: "vertical"
    padding: "14dp"
    spacing: "8dp"
    Label:
        text: "[b]MONU AI VOICE EDITOR[/b]\\n[size=13sp]Python • Voice Conversion Studio[/size]"
        markup: True
        size_hint_y: None
        height: "64dp"
    TextInput:
        id: api
        hint_text: "Cloud API URL"
        text: root.api_url
        multiline: False
        size_hint_y: None
        height: "48dp"
    Button:
        text: "API URL सेव करें"
        size_hint_y: None
        height: "44dp"
        on_release: root.save_api(api.text)
    Label:
        text: "1. अपनी अनुमति-प्राप्त आवाज़ का साफ WAV/MP3 sample चुनें"
        size_hint_y: None
        height: "45dp"
    Button:
        text: "Voice Sample चुनें"
        size_hint_y: None
        height: "48dp"
        on_release: root.choose_sample()
    Label:
        text: root.sample
        size_hint_y: None
        height: "36dp"
    Button:
        text: "Voice Profile के लिए Upload करें"
        size_hint_y: None
        height: "48dp"
        on_release: root.upload_sample()
    Label:
        text: "2. वह वीडियो चुनें जिसकी आवाज़ बदलनी है"
        size_hint_y: None
        height: "45dp"
    Button:
        text: "वीडियो चुनें"
        size_hint_y: None
        height: "48dp"
        on_release: root.choose_video()
    Label:
        text: root.video
        size_hint_y: None
        height: "36dp"
    Button:
        text: "मेरी आवाज़ में Convert करें"
        size_hint_y: None
        height: "52dp"
        on_release: root.convert()
    Label:
        text: root.status
        text_size: self.width, None
    Label:
        text: "नोट: यह starter है। वास्तविक conversion के लिए cloud GPU पर RVC model worker जोड़ना बाकी है।"
        text_size: self.width, None
        size_hint_y: None
        height: "55dp"
"""

class Root(BoxLayout):
    api_url = StringProperty("")
    sample = StringProperty("Sample नहीं चुना")
    video = StringProperty("Video नहीं चुना")
    status = StringProperty("Ready")

    def __init__(self, **kw):
        super().__init__(**kw)
        if CONFIG.exists():
            try: self.api_url = json.loads(CONFIG.read_text()).get("api_url", "")
            except Exception: pass

    def save_api(self, value):
        self.api_url = value.strip().rstrip("/")
        CONFIG.write_text(json.dumps({"api_url": self.api_url}))
        self.status = "API URL सेव हुआ"

    def choose_sample(self):
        filechooser.open_file(on_selection=lambda s: setattr(self, "sample", s[0] if s else self.sample),
                              filters=["*.wav", "*.mp3", "*.m4a", "*.flac"])

    def choose_video(self):
        filechooser.open_file(on_selection=lambda s: setattr(self, "video", s[0] if s else self.video),
                              filters=["*.mp4", "*.mov", "*.mkv"])

    def request(self, method, path, **kw):
        if not self.api_url: raise RuntimeError("पहले API URL सेव करें")
        return requests.request(method, self.api_url + path, timeout=600, **kw)

    def upload_sample(self):
        if not Path(self.sample).is_file():
            self.status = "पहले sample चुनें"; return
        threading.Thread(target=self._upload, daemon=True).start()

    def _upload(self):
        try:
            self.set_status("Sample upload हो रहा है...")
            with open(self.sample, "rb") as f:
                r = self.request("POST", "/v1/voice-profiles",
                    files={"audio": (Path(self.sample).name, f)},
                    data={"consent": "true"})
            r.raise_for_status()
            self.set_status("Upload response: " + str(r.json()))
        except Exception as e: self.set_status("Error: " + str(e))

    def convert(self):
        if not Path(self.video).is_file():
            self.status = "पहले वीडियो चुनें"; return
        threading.Thread(target=self._convert, daemon=True).start()

    def _convert(self):
        try:
            self.set_status("वीडियो cloud पर upload हो रहा है...")
            with open(self.video, "rb") as f:
                r = self.request("POST", "/v1/conversions",
                    files={"video": (Path(self.video).name, f)},
                    data={"profile_id": "REPLACE_WITH_PROFILE_ID",
                          "mode": "voice_conversion",
                          "preserve_timing": "true", "consent": "true"})
            r.raise_for_status()
            self.set_status("Job response: " + str(r.json()))
        except Exception as e: self.set_status("Error: " + str(e))

    def set_status(self, value):
        Clock.schedule_once(lambda dt: setattr(self, "status", value), 0)

class MonuApp(App):
    def build(self):
        Builder.load_string(KV)
        return Root()

if __name__ == "__main__": MonuApp().run()
