import os
import glob
import pickle
import subprocess
import math
import json

import ollama
from ddgs import DDGS
from sentence_transformers import SentenceTransformer


# -------------------------
# Settings
# -------------------------

def load_settings():

    if not os.path.exists("settings.json"):

        return {
            "auto_remember_info": True,
            "use_memory": True,
            "speak_answers": True,
            "memory_similarity_threshold": 0.65,
            "max_web_results": 5,
            "model": "qwen2.5:7b"
        }


    with open(
        "settings.json",
        "r"
    ) as f:

        return json.load(f)



settings = load_settings()


MODEL = settings["model"]


# -------------------------
# Paths
# -------------------------

MODEL_FOLDER = "./models"



# -------------------------
# Embedding model
# -------------------------

try:
    import torch

    if torch.cuda.is_available():
        DEVICE = "cuda"
    else:
        DEVICE = "cpu"

except:

    DEVICE = "cpu"



print(
    "Loading embedding model on:",
    DEVICE
)


embedder = SentenceTransformer(
    "all-MiniLM-L6-v2",
    device=DEVICE
)



# -------------------------
# Memory
# -------------------------

memory = []



def get_latest_model():

    files = glob.glob(
        f"{MODEL_FOLDER}/model*.pkl"
    )


    if not files:
        return None


    return max(
        files,
        key=os.path.getmtime
    )



def load_memory():

    global memory


    latest = get_latest_model()


    if latest:

        with open(
            latest,
            "rb"
        ) as f:

            memory = pickle.load(f)


        print(
            "Loaded memory:",
            latest
        )

        print(
            "Memories:",
            len(memory)
        )


    else:

        print(
            "No memory files found"
        )



def save_memory():

    os.makedirs(
        MODEL_FOLDER,
        exist_ok=True
    )


    files = glob.glob(
        f"{MODEL_FOLDER}/model*.pkl"
    )


    number = 1


    if files:

        nums = []

        for file in files:

            nums.append(
                int(
                    os.path.basename(file)
                    .replace("model", "")
                    .replace(".pkl", "")
                )
            )


        number = max(nums) + 1



    path = (
        f"{MODEL_FOLDER}/model{number}.pkl"
    )


    with open(
        path,
        "wb"
    ) as f:

        pickle.dump(
            memory,
            f
        )


    print(
        "Saved:",
        path
    )



def add_memory(question, answer):

    vector = embedder.encode(
        question
    ).tolist()


    memory.append(
        {
            "question": question,
            "answer": answer,
            "embedding": vector
        }
    )



def cosine_similarity(a, b):

    dot = sum(
        x*y
        for x, y in zip(a, b)
    )


    mag_a = math.sqrt(
        sum(
            x*x
            for x in a
        )
    )


    mag_b = math.sqrt(
        sum(
            x*x
            for x in b
        )
    )


    if mag_a == 0 or mag_b == 0:

        return 0


    return dot / (
        mag_a * mag_b
    )



def search_memory(question):

    if not memory:

        return None



    vector = embedder.encode(
        question
    ).tolist()



    best = None
    best_score = 0



    for item in memory:

        if "embedding" not in item:

            continue



        score = cosine_similarity(
            vector,
            item["embedding"]
        )



        if score > best_score:

            best_score = score
            best = item



    if best_score >= settings["memory_similarity_threshold"]:

        print(
            "Memory match:",
            round(best_score, 2)
        )


        return best["answer"]



    return None



# -------------------------
# Voice
# -------------------------

def speak(text):

    if not settings["speak_answers"]:

        return


    subprocess.run([
        "espeak-ng",
        "-v",
        "en-us+klatt",
        "-p",
        "1",
        "-s",
        "200",
        text
    ])



# -------------------------
# Web search
# -------------------------

def search_web(query):

    results = []


    with DDGS() as ddgs:

        for r in ddgs.text(
            query,
            max_results=settings["max_web_results"]
        ):

            results.append(
                r["body"]
            )


    return "\n".join(results)

# -------------------------
# Conversation memory
# -------------------------

conversation = []



# -------------------------
# AI
# -------------------------

def ask_ai(question):

    global conversation


    # Check saved memory first

    if settings["use_memory"]:

        old = search_memory(
            question
        )


        if old:

            print(
                "\nMemory:"
            )


            print(
                old
            )


            conversation.append(
                {
                    "role": "user",
                    "content": question
                }
            )


            conversation.append(
                {
                    "role": "assistant",
                    "content": old
                }
            )


            speak(
                old
            )


            return



    print(
        "\nSearching internet..."
    )


    web = search_web(
        question
    )



    conversation.append(
        {
            "role": "user",
            "content": question
        }
    )



    prompt = f"""
You are a helpful AI assistant.

Internet results:
{web}

Conversation history:
{conversation}

Rules:
- Understand references like "this", "that", and "it".
- Use previous messages if they relate.
- Answer clearly.
- Keep answers around one paragraph.
- If asked about code, explain how to use it and include the code.
"""



    print(
        "\nThinking...\n"
    )



    answer = ""



    stream = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        stream=True
    )



    for chunk in stream:

        text = chunk["message"]["content"]


        print(
            text,
            end="",
            flush=True
        )


        answer += text



    print()



    conversation.append(
        {
            "role": "assistant",
            "content": answer
        }
    )



    # Save memory

    if settings["auto_remember_info"]:

        add_memory(
            question,
            answer
        )


        save_memory()


    else:

        save = input(
            "\nSave this information? (y/n): "
        )


        if save.lower() in [
            "y",
            "yes"
        ]:

            add_memory(
                question,
                answer
            )


            save_memory()



    speak(
        answer
    )





# -------------------------
# Startup
# -------------------------

print(
    "AI Assistant"
)


use_models = input(
    "Use memory models? (y/n): "
)



if use_models.lower() in [
    "y",
    "yes"
]:

    load_memory()

else:

    print(
        "Memory disabled"
    )





# -------------------------
# Main loop
# -------------------------

while True:

    q = input(
        "\nYou: "
    )


    if q.lower() in [
        "exit",
        "quit"
    ]:

        break



    ask_ai(q)