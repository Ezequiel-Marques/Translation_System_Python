import socket
import sys

import speech_recognition as sr
from gtts import gTTS
import os


def listCodeLangs():
    return [
        'af: afrikaans',
        'sq: albanian',
        'am: amharic',
        'ar: arabic',
        'hy: armenian',
        'az: azerbaijani',
        'eu: basque',
        'be: belarusian',
        'bn: bengali',
        'bs: bosnian',
        'bg: bulgarian',
        'ca: catalan',
        'ceb: cebuano',
        'ny: chichewa',
        'zh-cn: chinese (simplified)',
        'zh-tw: chinese (traditional)',
        'co: corsican',
        'hr: croatian',
        'cs: czech',
        'da: danish',
        'nl: dutch',
        'en: english',
        'eo: esperanto',
        'et: estonian',
        'tl: filipino',
        'fi: finnish',
        'fr: french',
        'fy: frisian',
        'gl: galician',
        'ka: georgian',
        'de: german',
        'el: greek',
        'gu: gujarati',
        'ht: haitian creole',
        'ha: hausa',
        'haw: hawaiian',
        'iw: hebrew',
        'he: hebrew',
        'hi: hindi',
        'hm: hmong',
        'hu: hungarian',
        'is: icelandic',
        'ig: igbo',
        'id: indonesian',
        'ga: irish',
        'it: italian',
        'ja: japanese',
        'jw: javanese',
        'kn: kannada',
        'kk: kazakh',
        'km: khmer',
        'ko: korean',
        'ku: kurdish (kurmanji)',
        'ky: kyrgyz',
        'lo: lao',
        'la: latin',
        'lv: latvian',
        'lt: lithuanian',
        'lb: luxembourgish',
        'mk: macedonian',
        'mg: malagasy',
        'ms: malay',
        'ml: malayalam',
        'mt: maltese',
        'mi: maori',
        'mr: marathi',
        'mn: mongolian',
        'my: myanmar (burmese)',
        'ne: nepali',
        'no: norwegian',
        'or: odia',
        'ps: pashto',
        'fa: persian',
        'pl: polish',
        'pt: portuguese',
        'pa: punjabi',
        'ro: romanian',
        'ru: russian',
        'sm: samoan',
        'gd: scots gaelic',
        'sr: serbian',
        'st: sesotho',
        'sn: shona',
        'sd: sindhi',
        'si: sinhala',
        'sk: slovak',
        'sl: slovenian',
        'so: somali',
        'es: spanish',
        'su: sundanese',
        'sw: swahili',
        'sv: swedish',
        'tg: tajik',
        'ta: tamil',
        'te: telugu',
        'th: thai',
        'tr: turkish',
        'uk: ukrainian',
        'ur: urdu',
        'ug: uyghur',
        'uz: uzbek',
        'vi: vietnamese',
        'cy: welsh',
        'xh: xhosa',
        'yi: yiddish',
        'yo: yoruba',
        'zu: zulu']


# pip install SpeechRecognition
# pip install pyaudio
# pip install setuptools
def speech_recognition():
    global frase
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Diga alguma coisa: ")
        audio = recognizer.listen(source)

    try:
        frase = recognizer.recognize_google(audio, language='pt-BR')
        return frase
    except sr.UnknownValueError:
        print("Não foi possível entender a fala.")
        sys.exit()
    except sr.RequestError as e:
        print(f"Erro ao solicitar reconhecimento de fala; {e}")
        sys.exit()


# pip install gTTS
def speak(resposta: str, dest_lang):
    tts = gTTS(text=resposta, lang=dest_lang)
    tts.save("translated_audio.mp3")
    os.system("start translated_audio.mp3")


def menu_dest_lang():
    print("Escolha o código do idioma de destino no menu abaixo:")
    print("en => Inglês")
    print("pt => Português")
    print("de => Alemão")
    print("ja => Japonês")
    print("ko => Coreano")
    print("Em caso de dúvida, digite 'lista' para exibir todos os códigos:")
    print("Digite a linguagem de destino abaixo:")
    dest_lang = input()

    return dest_lang


def menu_principal():
    print("Selecione uma das opções abaixo para continuar:")
    print("1 - Traduzir de texto para texto")
    print("2 - Traduzir de aúdio para texto")
    print("3 - Traduzir de áudio para áudio")
    print("4 - Traduzir de texto para áudio")
    option = input("OPÇÃO: ")

    return option


def main():
    host = 'SERVER_IP'
    port = 12345

    code_langs = ""
    for code_lang in listCodeLangs():
        code_langs += code_lang + "\n"

    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            try:
                client_socket.connect((host, port))
                option = menu_principal()

                global text
                if option == "1":
                    text = input("Digite o texto para traduzir: ")
                    dest_lang = menu_dest_lang()
                    if dest_lang == "lista":
                        print(code_langs)
                        dest_lang = menu_dest_lang()
                elif option == "2":
                    print("ATENÇÃO! Nesta opção, a linguagem base é somente Português Brasil.")
                    dest_lang = menu_dest_lang()
                    if dest_lang == "lista":
                        print(code_langs)
                        dest_lang = menu_dest_lang()
                    text = speech_recognition()
                elif option == "3":
                    print("ATENÇÃO! Nesta opção, a linguagem base é somente Português Brasil.")
                    dest_lang = menu_dest_lang()
                    if dest_lang == "lista":
                        print(code_langs)
                        dest_lang = menu_dest_lang()
                    text = speech_recognition()
                elif option == "4":
                    text = input("Digite o texto para traduzir: ")
                    dest_lang = menu_dest_lang()
                    if dest_lang == "lista":
                        print(code_langs)
                        dest_lang = menu_dest_lang()
                else:
                    print("Opção inexistente!")
                    client_socket.close()
                    main()
                    break
                request = f"{text}|{dest_lang}"
                client_socket.sendall(request.encode('utf-8'))
                translated_text = client_socket.recv(1024).decode('utf-8')

                if option == "3" or option == "4":
                    speak(translated_text, dest_lang)
                else:
                    print("Texto traduzido:", translated_text)

            except Exception as e:
                print("Erro:", e)
            finally:
                client_socket.close()
            if input("Deseja continuar? (s/n): ").lower() != 's':
                break


if __name__ == "__main__":
    main()
