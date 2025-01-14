# LLaBot

## DISCLAIMER
This is a personal project, presented as-is, and is not intended for public use. It's very early in development, and there is no guarantee it will even function at the time of reading this. There are no plans to allow collaboration, feature requests, or other contributions.

## Current Features
**LLaBot** is a Python-based chatbot framework leveraging Hugging Face transformers to create dynamic and customizable conversational experiences. It combines advanced features like roleplay, integrations, and contextual efficiency to deliver innovative AI interactions.
- **Message Summarization**: Efficiently manage conversation context over time.
- **Customizable Personas and Roleplay**: Tailor bot behavior with personas, scenes, and other roleplay elements.
- **Weather Integration**: Get real-time weather updates with [OpenWeatherMap API](https://openweathermap.org/api).
- **Chess Play**: Interact with the bot while it simulates human-like chess play.
- **Planned Features**: Memory system for long-term context, additional integrations, and more!

## Installation

**LLaBot** leverages NVIDIA CUDA Toolkit 12.4. Follow the link below and install for your system:
- [NVIDIA CUDA Toolkit 12.4](https://developer.nvidia.com/cuda-12-4-0-download-archive)

Once installed, you will need to create a Python environment and install the appropriate packages. The following packages are needed:

- python=3.11
- pytorch
- torchvision
- torchaudio
- pytorch-cuda=12.4
- transformers
- nltk
- accelerate
- sentencepiece
- protobuf
- chess

Below is an example using Conda. It creates a new local environment and installs the packages.

```bash
$ conda create -p .venv python=3.11 pytorch torchvision torchaudio pytorch-cuda=12.4 -c pytorch -c nvidia
$ conda activate /path/to/env/
$ conda install transformers nltk accelerate sentencepiece protobuf chess
```

## Configuration
Configuration is currently handled via multiple JSON data files. Most are located in '*src/llabot/config*', with the exception being personas.
### config.json
Although user data can be created and used dynamically, it can also be loaded from a file. This is the default behavior, and this is the default file where that data is stored. This is also where you can toggle optional features, like the weather or the ability to play chess. On a side note, in order for weather to work properly you'll need an API key from OpenWeatherMap. Then, inconveniently, you need to edit this line in **llm_bot.py**:
```python
class LLMBot:
  api_key = "YOUR_API_KEY_HERE"
```
### presets.json
This is where you configure the various presets that a chat session can use for responding. For example, in the provided sample, the 'family' preset is given strict instructions and tight parameters that will guide it's responses. They must maintain this structure, but you can create whatever and however many presets you want.

### scene.json
This contains the default scene data that the bot will be presented with. It gives contexts to where it is, what your relationship is, and what the mood is. It must contain this structure, but the entries can be altered to your desire. Future plans exist to eventually allow multiple scene selection in a similar manner to multiple persona selection.

### persona.json
This is no *persona.json* itself, but rather persona data is managed through JSONs. A persona must have a folder and a JSON file with the same name. See the included '*generic/generic.json*' as an example. My recommendation would be to just copypasta it and change the entries for easy use.
## Usage
Included is '*src/app.py*' (and also an included launch file) that show example usage currently. It's obviously intended to be a backend, and the frontend will depend on end-user usage. The following is a simple example:
```python
from llabot import LLaBot, UserData

llabot = LLaBot() #Create an instance
user_data = UserData.from_json_file() #Load from file, but could just create normally.
llabot.add_bot(persona_name="generic") #Add bot with persona (can also change model type here)
llabot.start_chat(0, user_data) #Start a chat
print(llabot.generate_response(0, "Who was the 10th President of the United States?"))
```
## License
This project is licensed under the terms of the [GPL-3.0 license](LICENSE).

## Acknowledgments
- [Hugging Face Transformers](https://huggingface.co/transformers/)
- [OpenWeatherMap API](https://openweathermap.org/api)