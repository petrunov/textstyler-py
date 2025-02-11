import asyncio

import openai

from app.core.config import settings

openai.api_key = settings.OPENAI_API_KEY


async def llm_improvement(text: str) -> str:
    """
    Asynchronously calls the OpenAI Chat Completion API to improve text.
    Uses asyncio.to_thread to run the synchronous call without blocking.
    """
    try:
        response = await asyncio.to_thread(
            openai.chat.completions.create,
            messages=[
                {
                    "role": "system",
                    "content": "Improve the grammar and style of the following text.",
                },
                {"role": "user", "content": text},
            ],
            model="gpt-3.5-turbo",
        )
        improved_text = improved_text = response.choices[0].message.content.strip()
        return improved_text
    except Exception as e:
        return f"Error calling OpenAI API: {e}"


def llm_improvement_sync(text: str) -> str:
    """
    Synchronously calls the OpenAI Chat Completion API to improve text.
    """
    try:
        response = openai.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "Improve the grammar and style of the following text.",
                },
                {"role": "user", "content": text},
            ],
            model="gpt-3.5-turbo",
        )
        improved_text = improved_text = response.choices[0].message.content.strip()
        return improved_text
    except Exception as e:
        return f"Error calling OpenAI API: {e}"
