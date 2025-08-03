import rumps
import subprocess

class MajidRump(rumps.App):
    def __init__(self):
        super(MajidRump, self).__init__("😼 Majid")
        self.menu = ["Start Majid", "Quit Majid"]

    @rumps.clicked("Start Majid")
    def start_majid(self, _):
        # Replace with your virtualenv python path if needed
        subprocess.Popen(["/Users/taha/Documents/Python_codes/Majid/.venv/bin/python", "main.py"])

    @rumps.clicked("Quit Majid")
    def quit_majid(self, _):
        rumps.quit_application()

if __name__ == "__main__":
    MajidRump().run()
