import os
import discord
from discord.ext import commands

# ---------------- CONFIG ----------------
TOKEN = os.getenv("TOKEN")  # Must be set in Render Environment Variables
WELCOME_ROLE_ID = 1412416423652757556  # Role to assign

# ---------------- BOT SETUP ----------------
intents = discord.Intents.default()
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")


@bot.event
async def on_member_join(member: discord.Member):
    """Send DM embed with emojis + assign role"""

    # Build embed with your application emojis
    embed = discord.Embed(
        title="<a:main_heading:1415280147657003060> Welcome to EvX Corporation <a:main_heading:1415280147657003060>",
        description="We’re glad to have you here 🎉",
        color=0x3498db
    )

    embed.add_field(
        name="<a:features_heading:1415280020494094417> Rules",
        value="[Click Here](https://discord.com/channels/1412372622968225812/1412372623723069442)",
        inline=False
    )
    embed.add_field(
        name="<a:features_heading:1415280020494094417> Chat",
        value="[Join the Chat](https://discord.com/channels/1412372622968225812/1412381445108011049)",
        inline=False
    )
    embed.add_field(
        name="<a:features_heading:1415280020494094417> Buy",
        value="DM **@exhaust_xx** or [Create a Ticket](https://discord.com/channels/1412372622968225812/1415032580436394075)",
        inline=False
    )

    embed.set_footer(text="EvX Corporation • Enjoy your stay ✨")

    # Send DM
    try:
        await member.send(embed=embed)
        print(f"📩 Sent welcome embed to {member.name}")
    except discord.Forbidden:
        print(f"⚠️ Could not DM {member.name}")

    # Assign role
    try:
        role = member.guild.get_role(WELCOME_ROLE_ID)
        if role:
            await member.add_roles(role, reason="Auto Welcome Role")
            print(f"✅ Assigned role {role.name} to {member.name}")
        else:
            print("❌ Role not found. Check WELCOME_ROLE_ID.")
    except Exception as e:
        print(f"⚠️ Error assigning role: {e}")


# ---------------- RUN ----------------
if __name__ == "__main__":
    bot.run(TOKEN)
