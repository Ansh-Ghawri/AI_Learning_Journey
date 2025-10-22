from dotenv import load_dotenv
from openai import OpenAI
from openai import AsyncOpenAI
from openai.helpers import LocalAudioPlayer

import speech_recognition as sr
import asyncio

load_dotenv() 
client = OpenAI()
async_client = AsyncOpenAI()

async def tts(speech: str):
    async with async_client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="ash",
        input=speech,
        instructions="Speak in a cheerful,delighted and positive tone.",
        response_format="pcm",
    ) as response:
        await LocalAudioPlayer().play(response)


def main():
    r = sr.Recognizer() # Create a Recognizer instance(for recognizing speech)

    mic = sr.Microphone() # Create a Microphone instance(for accessing the microphone)
    with mic as source:
        r.adjust_for_ambient_noise(source) # Adjust for ambient noise
        r.pause_threshold = 2.0 # Set pause threshold

        SYSTEM_PROMPT = """
            You're an expert voice agent. You are given the transcript of what user has said using voice.
            You need to output as if you are an voice agent and whatever you speak
            will be converted back to audio using AI and played back to user.
        """
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]

        while True:
            print("Listening for speech...")
            audio = r.listen(source) # Listen for speech

            print("Processing audio... (STT)")
            stt = r.recognize_google(audio) # Convert speech to text using Google Web Speech API

            print("You said: " + stt) # Print the recognized text

            messages.append({"role": "user", "content": stt})

            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=messages,
            )

            reply = response.choices[0].message.content
            print("Agent's reply: " + reply)

            asyncio.run(tts(reply)) # Convert the agent's reply to speech and play it back

main()