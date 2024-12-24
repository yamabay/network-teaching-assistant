# network-teaching-assistant
Using langchain routing, the model can automatically determine the level of detail/expertise it should tailor its response to.

## Launch the Ollama Backend
```
docker-compose up -d
```
The Ollama backend will now be available at http://localhost:11434.

## Asking Questions to the Chain
Update the ```question``` variable in the ```network_assistant.py``` file with your question.
Execute the Python script:
```
python3 network_assistant.py
```
