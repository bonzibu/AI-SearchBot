# AI Voice Assistant

A local AI assistant powered by Ollama, web search, long-term memory, and text-to-speech.

The assistant can:
- Answer questions using a local LLM
- Search the internet when it does not know something
- Remember information between sessions
- Use downloadable memory packs
- Speak responses using eSpeak NG
- Understand follow-up questions using conversation context

---

# Features

## Local AI

This project uses Ollama to run the AI model locally.

Default model:

```
qwen2.5:7b
```

You can change the model in:

```
settings.json
```

---

## Memory System

The AI has two types of knowledge:

### Built-in AI knowledge

Provided by the Ollama model.

### Memory files

Stored in:

```
./models/
```

Memory files contain information the AI has learned.

Example:

```
models/
├── model1.pkl
├── model2.pkl
└── model3.pkl
```

The newest memory file is automatically loaded.

---

# Installation

## Requirements

You need:

- Python 3.10+
- Ollama
- eSpeak NG

---

## Install Python packages

Run:

```bash
pip install -r requirements.txt
```

---

## Install Ollama

Download Ollama:

```
https://ollama.com
```

Then download the AI model:

```bash
ollama pull qwen2.5:7b
```

---

## Install eSpeak NG

Download eSpeak NG:

```
https://github.com/espeak-ng/espeak-ng
```

Make sure it works:

```bash
espeak-ng --version
```

---

# Running The Assistant

Start the AI:

```bash
python tts.py
```

You will see:

```
Use memory models? (y/n):
```

Choose:

```
y
```

to load files from:

```
./models/
```

or:

```
n
```

to start without saved memory.

---

# Learning New Information

When the AI finds new information, it can save it to memory.

The setting:

```json
"auto_remember_info": true
```

means:

```
AI learns automatically
```

No confirmation is needed.

If changed to:

```json
"auto_remember_info": false
```

the AI will ask:

```
Save this information? (y/n)
```

---

# Downloading Pre-Trained Memory Packs

You can download optional pre-trained memory files here:

```
https://example.com
```

After downloading:

1. Put the `.pkl` file inside:

```
./models/
```

Example:

```
models/
└── SCP_memory.pkl
```

2. Start the assistant:

```bash
python tts.py
```

3. Select:

```
Use memory models? (y/n): y
```

The assistant will automatically use the memory.

---

# Settings

Edit:

```
settings.json
```

Example:

```json
{
    "auto_remember_info": true,
    "use_memory": true,
    "speak_answers": true,
    "memory_similarity_threshold": 0.65,
    "max_web_results": 5,
    "model": "qwen2.5:7b"
}
```

## Options

### auto_remember_info

Automatically save new information.

```json
true
```

or

```json
false
```

---

### use_memory

Enable saved memory files.

```json
true
```

---

### speak_answers

Enable text-to-speech.

```json
true
```

---

### memory_similarity_threshold

Controls how closely a question must match saved information.

Lower:

```
0.5
```

More matches but less accurate.

Higher:

```
0.8
```

Fewer matches but more accurate.

---

# Folder Structure

Recommended setup:

```
AI Assistant/
│
├── tts.py
├── requirements.txt
├── settings.json
│
└── models/
    ├── model1.pkl
    └── model2.pkl
```

---

# Troubleshooting

## Ollama model not found

Run:

```bash
ollama pull qwen2.5:7b
```

---

## No voice output

Check:

```bash
espeak-ng --version
```

---

## Memory not loading

Make sure files are inside:

```
./models/
```

and are `.pkl` files.

---

# License

Free to modify and use.
