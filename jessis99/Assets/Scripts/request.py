import requests

import sys

# Server-IP
LM_API_URL = "http://136.199.51.131:1234/v1/chat/completions"
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": "Bearer lm-studio"
}

# Hier gibst du das Modell an, das du nutzen willst
MODEL_NAME = "deepseek-coder-v2-lite-instruct"

def send_prompt(prompt):
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    try:
        response = requests.post(LM_API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()

    except requests.exceptions.RequestException as e:
        print("\n Netzwerk- oder Serverfehler:", e)
        return None
    except KeyError:
        print("\n Antwort konnte nicht gelesen werden.")
        return None

if __name__ == "__main__":
 # Wenn ein Prompt übergeben wurde (z. B. aus Unity)
    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])
        reply = send_prompt(prompt)
        if reply:
            print("\nModell-Antwort:\n" + reply)
    else:
        # Interaktive Schleife nur, wenn kein Argument übergeben wurde
        print("Chat mit LM Studio über http://136.199.51.131:1234")
        print("Gib deinen Prompt ein (oder 'exit' zum Beenden).")

        while True:
            try:
                prompt = input("\nDu: ")
            except EOFError:
                print("\nEingabe abgebrochen.")
                break

            if prompt.lower() in ["exit", "quit"]:
                print("Chat beendet.")
                break

            reply = send_prompt(prompt)
            if reply:
                print("\nModell-Antwort:\n" + reply)