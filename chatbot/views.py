from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from groq import Groq
from dotenv import load_dotenv


import os
import json

load_dotenv()
print(os.getenv("GROQ_API_KEY"))
client = Groq(

    api_key=os.getenv("GROQ_API_KEY")

)


def home(request):

    return render(request, 'index.html')


@csrf_exempt
def chat(request):

    if request.method == "POST":

        try:

            data = json.loads(request.body)

            user_message = data.get('message')

            prompt = f"""
            You are a helpful medical AI assistant.

            Patient:
            {user_message}

            Give short professional advice.
            """

            print("Sending request to Groq...")

            completion = client.chat.completions.create(

                model="llama-3.3-70b-versatile",

                messages=[
                    {
                        "role":"user",
                        "content":prompt
                    }
                ]

            )

            print("Groq response received")

            ai_reply = completion.choices[0].message.content

            return JsonResponse({

                "reply": ai_reply

            })

        except Exception as e:

           import traceback

           traceback.print_exc()

           return JsonResponse({

             "reply": str(e)

    })