## Instagram AI Chatbot
> AI-powered bot, which responds to messages sent to your Instagram account in real-time. 
> All you have to do is specify a [instructions](https://github.com/aensse/instagram_chatbot/blob/main/instructions.txt) for it.

## Quick start
For now, it's only suitable for use by developers. It requires [Instagram MQTT](https://github.com/Nerixyz/instagram_mqtt) script, which will send all messages to our API in original JSON format. Full integration with MQTT is coming soon.

I strongly recommend using [uv](https://docs.astral.sh/uv/), as further steps will be based on this package manager.

1) In the OS console (assuming you are in the folder where you want to keep the project), type:
```
git clone https://github.com/aensse/instagram_chatbot
cd insta-ai
uv sync
cp .env-example .env
```

2) Fill .env with your data:
- xAI API key – get one [here](https://console.x.ai/)
- Instagram credentials - just a data for a Instagram account

3) Run the server:
```
uv run fastapi dev
```

For now, every message delivered to /api/v1/messages endpoint will be responded. As said before, it requires [Instagram MQTT](https://github.com/Nerixyz/instagram_mqtt) script, which listens for new messages and sends them to our API. It will be implemented in the future.

## AI Instructions
The whole personality of the bot and the way it carries on a conversation should be defined in the
[instructions](https://github.com/aensse/instagram_chatbot/blob/main/instructions.txt) file. 

You can also specify when it should end the conversation.

## Tech behind

Application is asynchronous and built on top of the [FastAPI](https://github.com/fastapi/fastapi). 

A flow of message responding process is like so:
- if new message arrives it's validated using [Pydantic](https://github.com/pydantic/pydantic),
- then [FastAPI Background Task](https://fastapi.tiangolo.com/tutorial/background-tasks/) is created,
- it checks for conversation status in database using [SQLAlchemy](https://docs.sqlalchemy.org/en/20/),
- by using [aiograpi](https://github.com/subzeroid/aiograpi), the bot gets the entire context of the conversation and passes it to AI analysis,
- thanks to pre-prepared AI instructions and a connection to the [Grok API](https://console.x.ai/), a personalized response is generated,
- the whole process ends with direct message to the user.


> Keep in mind that a bot uses third-party scripts that may violate Instagram's terms of use. 
> You use it at your own risk. 











