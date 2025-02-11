import asyncio

import openai

from app.core.config import settings

openai.api_key = settings.OPENAI_API_KEY

PROMPT_INSTRUCTIONS = (
    "Please improve the grammar and style of the text provided below. Always respond with text "  # noqa E501
    "improvements. If you are unable to improve the text for any reason, simply return the message: "  # noqa E501
    "'Cannot improve text because of: <reason>. Please try again.' Do not engage in any other conversation; "  # noqa E501
    "only improve the text when possible, and if improvement cannot be performed, return an error message."  # noqa E501
)


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
                    "content": PROMPT_INSTRUCTIONS,
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
                    "content": PROMPT_INSTRUCTIONS,
                },
                {"role": "user", "content": text},
            ],
            model="gpt-3.5-turbo",
        )
        improved_text = improved_text = response.choices[0].message.content.strip()
        return improved_text
    except Exception as e:
        return f"Error calling OpenAI API: {e}"
