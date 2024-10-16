# Using OpenAI

```python
from openai import OpenAI

client = OpenAI(
    api_key="<API_KEY>",
    base_url="https://litellm.govtext.gov.sg/",
    default_headers={"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"},
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "hello",
        }
    ],
    model="gpt-4o-prd-gcc2-lb",
)
```

# Using LangChain

```python
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

chat = ChatOpenAI(
    api_key="<API_KEY>",
    openai_api_base="https://litellm.govtext.gov.sg/",
    model = "gpt-4o-prd-gcc2-lb",
    temperature=0.1,
    default_headers={"user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/81.0"},
)

messages = [
    SystemMessage(
        content="You are a helpful assistant"
    ),
    HumanMessage(
        content="hello"
    ),
]
response = chat(messages)
```

# Using Python requests library

```python
import requests

input_json = {
    "model": "gpt-4o-prd-gcc2-lb",
    "messages": [
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "hello"}
    ],
}

response = requests.post(
    url="https://litellm.govtext.gov.sg/chat/completions",
    json=input_json,
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer <API_KEY>", # API Key here
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/81.0"
    })
```


# Available Model Names
Refer to the "id" in the following data:
```
{
  "data": [
    {
      "id": "gpt-4o-mini-prd-gcc2-lb",
      "object": "model",
      "created": 1677610602,
      "owned_by": "openai"
    },
    {
      "id": "text-embedding-3-large-prd-gcc2-lb",
      "object": "model",
      "created": 1677610602,
      "owned_by": "openai"
    },
    {
      "id": "gpt-4-prd-gcc2-lb",
      "object": "model",
      "created": 1677610602,
      "owned_by": "openai"
    },
    {
      "id": "gpt-35-turbo-prd-gcc2-lb",
      "object": "model",
      "created": 1677610602,
      "owned_by": "openai"
    },
    {
      "id": "text-embedding-3-small-prd-gcc2-lb",
      "object": "model",
      "created": 1677610602,
      "owned_by": "openai"
    },
    {
      "id": "gpt-4o-prd-gcc2-lb",
      "object": "model",
      "created": 1677610602,
      "owned_by": "openai"
    }
  ],
  "object": "list"
}
```
