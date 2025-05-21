import speech_recognition as sr
from gtts import gTTS as g
import io
from pygame import mixer

# Função responsável por falar 
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

# Função responsável por ouvir
def ouvir_microfone():
    # Habilita o microfone para ouvir o usuario
    microfone = sr.Recognizer()
    with sr.Microphone() as source:
        # Chama a funcao de reducao de ruido
        microfone.adjust_for_ambient_noise(source)
        # Avisa ao usuario que esta pronto para ouvir
        falar("Diga alguma coisa")
        # Armazena o audio
        audio = microfone.listen(source)
    
    try:
        frase = microfone.recognize_google(audio, language='pt-BR').lower()
        print("Você disse: " + frase)

        # Filtro de palavras
        palavras_feias = ['pt', 'partido dos trabalhadores']
        presidentes_proibidos = ['dilma', 'lula']
        resposta_sensata_partido = "Primeiramente proibido falar esse partido aqui, somos fechados com o Bolsonaro!"

        for palavra in palavras_feias:
            if palavra in frase:
                frase = resposta_sensata_partido
        for palavrao in presidentes_proibidos:
            if 'dilma' in frase:
                frase = 'Essa aí afundou o brasil'
            elif 'lula' in frase:
                frase = 'Esse aí afundou o brasil e é pai dos burros'
        return frase
        
    except sr.UnknownValueError:
        print("Não entendi")
        return None

frase = ouvir_microfone()
if frase:
    falar(frase)