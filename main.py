from aiogram import Bot, types, executor, Dispatcher
import config
import asyncio

from parser import parse


bot = Bot(token=config.settings['TOKEN'], parse_mode=types.ParseMode.HTML)

dp = Dispatcher(bot)
posts = []
page_post = 0


@dp.message_handler()
async def post_content(message: types.Message):
    global page_post
    while True:
        data, pages_parse = parse(posts=posts, page_post=page_post)
        data = data[0]
        # await asyncio.sleep(15)

        if data['Title'] not in posts:
            chat_id = message.chat.id
            posts.append(data['Title'])
            text = f'{data["Title"]}\n{data["URL"]}'

            page_post = pages_parse

            await bot.send_message(chat_id=chat_id, text=text)


executor.start_polling(dp)
