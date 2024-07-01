from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
import aiohttp
import asyncio

# Initialize the bot and dispatcher
API_TOKEN = '7360335399:AAHe6XYUGLBiZR9RGn9YIApJXxrZyabVDCM'
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

async def fetch_data():
    url = 'https://pokeapi.co/api/v2/pokemon?limit=12&offset=0'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            return data['results']  # Return the list of pokemons

async def inline_pokes(pokemons):
    keyboard = InlineKeyboardBuilder()
    for pokemon in pokemons:
        keyboard.add(InlineKeyboardButton(text=pokemon["name"], callback_data=pokemon["url"]))
    return keyboard.adjust(1).as_markup()  # Return the InlineKeyboardMarkup

async def fetch_pokemon_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

@dp.callback_query(F.data.regexp(r"^https:\/\/pokeapi\.co\/api\/v2\/pokemon\/\d+\/$"))
async def pokemon_info(callback: CallbackQuery):
    await callback.answer()  # Acknowledge the callback immediately
    pokemon_url = callback.data
    
    # Fetch specific Pokémon data
    pokemon_data = await fetch_pokemon_data(pokemon_url)
    pokemon_image = pokemon_data['sprites']['other']['official-artwork']['front_default']
    pokemon_name = pokemon_data['name']
    
    # Send Pokémon image and name
    await callback.message.reply_photo(photo=pokemon_image, caption=f'You selected: {pokemon_name}')

@dp.message(CommandStart())
async def cmd_start(message: Message):
    pokemons = await fetch_data()
    keyboard = await inline_pokes(pokemons)
    await message.reply(f'Hello, {message.from_user.username}. Choose a Pokémon:', reply_markup=keyboard)

# Start polling
if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))
