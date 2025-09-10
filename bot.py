# bot.py
import os
import discord
from discord.ext import commands
from discord import app_commands
from flask import Flask
import threading

# ---------------- CONFIG ----------------
TOKEN = os.getenv("TOKEN")  # Set this in Render environment variables
WELCOME_ROLE_ID = 1412416423652757556

# Read welcome message from file
with open("welcome.txt", "r", encoding="utf-8") as f:
    WELCOME_MESSAGE = f.read()

# ---------------- DISCORD BOT ----------------
intents = discord.Intents.default()
intents.members = True  # required for member join event
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")

@bot.event
async def on_member_join(member: discord.Member):
    try:
        # Assign the role
        role = member.guild.get_role(WELCOME_ROLE_ID)
        if role:
            await member.add_roles(role, reason="Auto Welcome Role")

        # Send DM with embed
        embed = discord.Embed(
            title="👋 Welcome!",
            description=WELCOME_MESSAGE,
            color=discord.Color.blue()
        )
        embed.set_footer(text=f"Welcome to {member.guild.name}!")
        await member.send(embed=embed)
        print(f"✅ Welcome DM sent to {member.name}")

    except Exception as e:
        print(f"❌ Error in on_member_join: {e}")

# ---------------- FLASK KEEP-ALIVE ----------------
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_web():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    thread = threading.Thread(target=run_web)
    thread.start()

# ---------------- START ----------------
if __name__ == "__main__":
    keep_alive()
    bot.run(TOKEN)
