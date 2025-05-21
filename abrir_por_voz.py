from importar import *
# Mapeamento de aplicativos (personalize conforme suas necessidades)
APP_MAPPING = {
    'chrome': {
        'windows': 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
    },
    'vscode': {
        'windows': 'code'
    }
}

def falar(text):
    tts = g(text=text, lang='pt')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    
    mixer.init()
    mixer.music.load(fp)
    mixer.music.play()
    while mixer.music.get_busy():
        continue
    
def get_os_specific_command(app_name):
    system = platform.system().lower()
    app_config = APP_MAPPING.get(app_name.lower(), {})
    
    if system in app_config:
        command = app_config[system]
        if '{username}' in command:
            command = command.format(username=os.getlogin())
        return command
    return None

def open_application(app_name):
    command = get_os_specific_command(app_name)
    
    if command:
        try:
            if platform.system() == 'Windows':
                subprocess.Popen(command, shell=True)
            else:
                os.system(command)
            falar(f"Abriu {app_name} com sucesso!")
            return True
        except Exception as e:
            falar(f"Erro ao abrir {app_name}: {e}")
            return False
    else:
        falar(f"ops, Aplicativo {app_name} não configurado")
        return False

def abrir_com_comando():
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        falar("Aguardando comando...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, timeout=8)
        
        try:
            command = recognizer.recognize_google(audio, language='pt-BR').lower()
            falar(f"Comando reconhecido: {command}")
            
            # Verifica comandos para abrir aplicativos
            if 'abrir' in command or 'iniciar' in command or 'open' in command:
                app_name = command.split('abrir')[-1].split('iniciar')[-1].strip()
                
                if not open_application(app_name):
                    # Se não encontrou o app, tenta abrir como site
                    falar(f'Abrindo site referente ao comando')
                    webbrowser.open(f"https://{app_name}.com")
            elif 'sair' in command or 'encerrar' in command:
                sys.exit(0)
            else:
                falar("Comando não reconhecido. Tente dizer 'Abrir [nome do aplicativo]'")
                
        except sr.UnknownValueError:
            falar("Não entendi o comando")
        except sr.RequestError:
            falar("Erro ao acessar serviço de reconhecimento de voz")
        except sr.WaitTimeoutError:
            falar("Tempo de espera esgotado")

if __name__ == "__main__":
    
    falar("Sistema de Abertura por Voz")
    
    while True:
        abrir_com_comando()
        sleep(1)