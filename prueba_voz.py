import pyttsx3 as tts


engine = tts.init()
engine.setProperty('rate', 145)
engine.setProperty('voice', 'spanish')
engine.say("Modo sexo: activado")
engine.runAndWait()

voces = engine.getProperty('voices')


# for voice in voces:
#    engine.setProperty('voice', voice.id)
#    print(voice.id)
#    engine.say('Modo sexo activado')
# engine.runAndWait()