from gtts import gTTS
from playsound3 import playsound

def text_to_speech(text):
    res = gTTS(text=text, lang='en', tld='co.uk')
    filename = "output.mp3"
    res.save(filename)
    playsound(filename)

if __name__ == "__main__":
    text = "Hello, I am GeeksforGeeks and I made a Speech Synthesis System With Python."
    text_to_speech(text)

