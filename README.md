# network-teaching-assistant
Using langchain routing, the model can automatically determine the level of detail/expertise it should tailor its response to based on the user's question.

The first step in the chain will return either "beginner" or "expert" by assessing the question's difficulty.
Based on what the first step returns will determine whether the beginner or expert chain is ran. 

These chains are identical except for the prompt passed to the model.

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
