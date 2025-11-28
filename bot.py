
import logging
from os import getenv

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from openai import OpenAI
from openai import APIConnectionError, APIError


# Configure logging
logging.basicConfig(level=logging.INFO)


API_TOKEN = "8323913052:AAFGKxQD4tAKIhdLocMG5LrhPZZal1otYcU"
OPENAI_API_KEY = "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"

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher()
client = OpenAI(api_key=OPENAI_API_KEY, base_url="https://openrouter.ai/api/v1")


@dp.message(CommandStart())
async def command_start_handler(message: types.Message):
    logging.info(f"Received /start from {message.from_user.full_name}")
    await message.answer(f"Привет, {message.from_user.full_name}! \n Я нейросеть peekseek. Отправь мне сообщение, и я отвечу.")


@dp.message(F.text.lower().contains("кто тебя разработал"))
@dp.message(F.text.lower().contains("кто твой разработчик"))
@dp.message(F.text.lower().contains("кем ты был разработан"))
async def handle_developer_question(message: types.Message):
    logging.info(f"Received developer question from {message.from_user.full_name}: {message.text}")
    await message.answer("Я был разработан разработчиком lebeday.")


@dp.message(F.text)
async def handle_message(message: types.Message):
    logging.info(f"Received message from {message.from_user.full_name}: {message.text}")
    try:
        completion = client.chat.completions.create(
            model="google/gemini-2.5-flash",
            messages=[
                {"role": "user", "content": message.text}
            ],
            temperature=0.7,
            max_tokens=500, # Уменьшено для ускорения ответов
            top_p=1,
        )
        response_text = completion.choices[0].message.content
        logging.info(f"Sending response to {message.from_user.full_name}: {response_text}")
        await message.answer(response_text)
    except APIConnectionError as e:
        logging.error(f"Ошибка подключения к API OpenRouter: {e}")
        await message.answer(f"Ошибка подключения к API OpenRouter: {e}")
    except APIError as e:
        logging.error(f"Ошибка API OpenRouter: {e}")
        await message.answer(f"Ошибка API OpenRouter: {e}")
    except Exception as e:
        logging.error(f"Произошла неизвестная ошибка: {e}")
        await message.answer(f"Произошла неизвестная ошибка: {e}")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
