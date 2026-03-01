# First steps
Install all required dependencies
```bash
cd MedManager
python3 -m venv .venv
pip install -r requirements.txt
```
Run redis in docker
```bash
docker compose up
```
Set up all environment settings see env_example

# Running the bot
```bash
python3 main.py
```

# Bot interaction
- `/start` - User entrypoint
- `Проверить клиентов` - check clients
- Other interaction is handled with LLM