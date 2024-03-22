from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.network.urlrequest import UrlRequest
from kivy.core.audio import SoundLoader
import zipfile
import shutil
import requests
import os
import ctypes
import sys
import time

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    sys.exit(0)


Window.size = (600, 400)

KV = '''
<CustomButton@Button>:
    background_color: (0, 0, 0, 0)
    canvas.before:
        Color:
            rgba: (0.1, 0.5, 0.6, 1) if self.state == 'normal' else (0.1, 0.5, 0.6, 0.5)
        RoundedRectangle:
            size: self.size
            pos: self.pos
            radius: [10]

BoxLayout:
    orientation: 'vertical'
    spacing: 10
    padding: 10

    Image:
        source: 'launcher_background.png' 
        allow_stretch: True
        keep_ratio: False
        size_hint: (1, 1)

    Label:
        id: status_label
        text: 'Verificando atualizações...'
        size_hint_y: None
        height: 40

    ProgressBar:
        id: progress_bar
        max: 100
        value: 0
        size_hint_y: None
        height: 20

    BoxLayout:
        size_hint_y: None
        height: 50
        spacing: 10

        CustomButton:
            text: 'Atualizar'
            id: update_button
            on_press: app.check_for_updates()

        CustomButton:
            text: 'Iniciar'
            id: start_button
            disabled: True  
            on_press: app.start_application()
'''

class LauncherApp(App):
    def __init__(self, **kwargs):
        super(LauncherApp, self).__init__(**kwargs)
        self.local_version_file = "version.txt"
        self.local_version = self.get_local_version()
        self.project_zip_url = 'https://github.com/OTCv8/otclientv8/archive/refs/heads/master.zip' #Link arquivo do Client .zip
        self.title = 'NOME DO SEU OT AQUI'
        self.background_music = SoundLoader.load('background_music.ogg')

    def build(self):
        return Builder.load_string(KV)

    def on_start(self):
        self.check_for_updates()
        if self.background_music:
            self.background_music.volume = 0.07
            self.background_music.loop = True
            self.background_music.play()

    def find_executable(self, start_path, executable_name):
        for dirpath, dirnames, filenames in os.walk(start_path):
            if executable_name in filenames:
                return os.path.join(dirpath, executable_name)
        return None

    def start_application(self):
        executable_path = self.find_executable(os.getcwd(), 'otclient_dx.exe')
        if executable_path and os.path.isfile(executable_path):
            os.startfile(executable_path)
            time.sleep(3)
            self.stop()
        else:
            self.root.ids.status_label.text = 'otclient_dx.exe não encontrado.'

    def check_for_updates(self):
        url = 'https://raw.githubusercontent.com/tonireinbold/Compilador-Python-to-EXE/main/version.txt'  # Controle de Versão
        UrlRequest(url, on_success=self.on_version_check_success, on_failure=self.on_version_check_failure)

    def on_version_check_success(self, req, result):
        latest_version = result.strip()

        if latest_version > self.local_version:
            self.root.ids.status_label.text = 'Atualização disponível!'
            self.root.ids.progress_bar.value = 50
            self.root.ids.start_button.disabled = True
            self.root.ids.update_button.disabled = False
            self.download_and_extract_project(latest_version)
        else:
            self.root.ids.status_label.text = 'Atualizado!'
            self.root.ids.progress_bar.value = 100
            self.root.ids.start_button.disabled = False
            self.root.ids.update_button.disabled = True

    def on_version_check_failure(self, req, result):
        self.root.ids.status_label.text = 'Falha ao verificar atualizações.'

    def get_local_version(self):
        if not os.path.exists(self.local_version_file):
            with open(self.local_version_file, 'w') as file:
                file.write("1.0")
            return "1.0"
        else:
            with open(self.local_version_file, 'r') as file:
                return file.read().strip()

    def update_local_version(self, new_version):
        with open(self.local_version_file, 'w') as file:
            file.write(new_version)

    def download_and_extract_project(self, latest_version):
        try:
            response = requests.get(self.project_zip_url, stream=True)
            if response.status_code == 200:
                zip_path = os.path.join(os.getcwd(), 'project.zip')
                with open(zip_path, 'wb') as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(os.getcwd())
                os.remove(zip_path)

                self.update_local_version(latest_version)
                self.root.ids.status_label.text = 'Aplicativo atualizado com sucesso!'
                self.root.ids.progress_bar.value = 100
                self.root.ids.start_button.disabled = False
            else:
                self.root.ids.status_label.text = 'Falha ao baixar a atualização.'
        except Exception as e:
            self.root.ids.status_label.text = f'Erro ao atualizar: {e}'

if __name__ == '__main__':
    LauncherApp().run()

    #thanks
