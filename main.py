import discord
from discord.ext import commands, tasks
import asyncio
import os
from datetime import datetime, timedelta, timezone
import logging
from dotenv import load_dotenv
from typing import Optional
import json

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot setup with intents
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Configuration file for auto-cleanup settings
CONFIG_FILE = "bot_config.json"


def load_config():
    """Load bot configuration from JSON file"""
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"auto_cleanup": {}, "cleanup_age_days": 7, "cleanup_enabled": False}


def save_config(config):
    """Save bot configuration to JSON file"""
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)


config = load_config()


@bot.event
async def on_ready():
    """Event triggered when bot is ready"""
    print(f"{bot.user} has connected to Discord!")
    print(f"Bot is in {len(bot.guilds)} guilds")

    # Load cogs
    try:
        await bot.load_extension("cogs.advanced_utils")
        print("Advanced utilities cog loaded successfully")
    except Exception as e:
        print(f"Failed to load advanced utilities cog: {e}")

    try:
        await bot.load_extension("cogs.help")
        print("Help cog loaded successfully")
    except Exception as e:
        print(f"Failed to load help cog: {e}")

    # Start auto cleanup task if enabled
    if config.get("cleanup_enabled", False):
        auto_cleanup.start()
        print("Auto cleanup task started")


@bot.command(name="clear")
@commands.has_permissions(manage_messages=True)
async def clear_messages(ctx, amount: int = 10):
    """Clear a specified number of messages from the current channel"""
    if amount <= 0:
        await ctx.send("❌ Please specify a positive number of messages to delete.")
        return

    if amount > 100:
        await ctx.send("❌ Cannot delete more than 100 messages at once.")
        return

    try:
        deleted = await ctx.channel.purge(
            limit=amount + 1
        )  # +1 to include the command message
        await ctx.send(f"✅ Deleted {len(deleted) - 1} messages.", delete_after=5)
        logger.info(
            f"Cleared {len(deleted) - 1} messages in {ctx.channel.name} by {ctx.author}"
        )
    except discord.Forbidden:
        await ctx.send("❌ I don't have permission to delete messages in this channel.")
    except discord.HTTPException as e:
        await ctx.send(f"❌ An error occurred: {e}")


@bot.command(name="clearall")
@commands.has_permissions(administrator=True)
async def clear_all_messages(ctx):
    """Clear all messages in the current channel (Admin only)"""
    await ctx.send(
        "⚠️ This will delete ALL messages in this channel. Type `confirm` within 10 seconds to proceed."
    )

    def check(m):
        return (
            m.author == ctx.author
            and m.channel == ctx.channel
            and m.content.lower() == "confirm"
        )

    try:
        await bot.wait_for("message", check=check, timeout=10.0)
    except asyncio.TimeoutError:
        await ctx.send("❌ Command cancelled - no confirmation received.")
        return

    try:
        deleted = 0
        async for message in ctx.channel.history(limit=None):
            await message.delete()
            deleted += 1
            if deleted % 10 == 0:  # Progress update every 10 deletions
                print(f"Deleted {deleted} messages...")

        await ctx.send(f"✅ Deleted all {deleted} messages from this channel.")
        logger.info(
            f"Cleared all {deleted} messages in {ctx.channel.name} by {ctx.author}"
        )
    except discord.Forbidden:
        await ctx.send("❌ I don't have permission to delete messages in this channel.")
    except discord.HTTPException as e:
        await ctx.send(f"❌ An error occurred: {e}")


@bot.command(name="clearuser")
@commands.has_permissions(manage_messages=True)
async def clear_user_messages(ctx, user: discord.Member, amount: int = 10):
    """Clear messages from a specific user"""
    if amount <= 0:
        await ctx.send("❌ Please specify a positive number of messages to delete.")
        return

    if amount > 100:
        await ctx.send("❌ Cannot search more than 100 messages at once.")
        return

    def check(m):
        return m.author == user

    try:
        deleted = await ctx.channel.purge(limit=amount * 2, check=check)
        await ctx.send(
            f"✅ Deleted {len(deleted)} messages from {user.mention}.", delete_after=5
        )
        logger.info(
            f"Cleared {len(deleted)} messages from {user} in {ctx.channel.name} by {ctx.author}"
        )
    except discord.Forbidden:
        await ctx.send("❌ I don't have permission to delete messages in this channel.")
    except discord.HTTPException as e:
        await ctx.send(f"❌ An error occurred: {e}")


@bot.command(name="clearold")
@commands.has_permissions(manage_messages=True)
async def clear_old_messages(ctx, days: int = 7):
    """Clear messages older than specified days"""
    if days <= 0:
        await ctx.send("❌ Please specify a positive number of days.")
        return

    cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)

    def check(m):
        return m.created_at < cutoff_date

    try:
        deleted = await ctx.channel.purge(limit=None, check=check, before=cutoff_date)
        await ctx.send(
            f"✅ Deleted {len(deleted)} messages older than {days} days.",
            delete_after=5,
        )
        logger.info(
            f"Cleared {len(deleted)} old messages in {ctx.channel.name} by {ctx.author}"
        )
    except discord.Forbidden:
        await ctx.send("❌ I don't have permission to delete messages in this channel.")
    except discord.HTTPException as e:
        await ctx.send(f"❌ An error occurred: {e}")


@bot.command(name="stats")
async def server_stats(ctx):
    """Get comprehensive server statistics"""
    guild = ctx.guild

    # Basic server info
    embed = discord.Embed(
        title=f"📊 Server Statistics for {guild.name}",
        color=discord.Color.blue(),
        timestamp=datetime.now(),
    )

    embed.set_thumbnail(url=guild.icon.url if guild.icon else None)

    # Member stats
    total_members = guild.member_count
    online_members = len(
        [m for m in guild.members if m.status != discord.Status.offline]
    )
    bots = len([m for m in guild.members if m.bot])
    humans = total_members - bots

    embed.add_field(
        name="👥 Members",
        value=f"Total: {total_members}\nHumans: {humans}\nBots: {bots}\nOnline: {online_members}",
        inline=True,
    )

    # Channel stats
    text_channels = len(guild.text_channels)
    voice_channels = len(guild.voice_channels)
    categories = len(guild.categories)

    embed.add_field(
        name="📝 Channels",
        value=f"Text: {text_channels}\nVoice: {voice_channels}\nCategories: {categories}",
        inline=True,
    )

    # Role and emoji stats
    roles = len(guild.roles)
    emojis = len(guild.emojis)

    embed.add_field(
        name="🎭 Other", value=f"Roles: {roles}\nEmojis: {emojis}", inline=True
    )

    # Server info
    embed.add_field(
        name="ℹ️ Server Info",
        value=f"Created: {guild.created_at.strftime('%B %d, %Y')}\nOwner: {guild.owner.mention if guild.owner else 'Unknown'}\nBoost Level: {guild.premium_tier}",
        inline=False,
    )

    await ctx.send(embed=embed)


@bot.command(name="channelstats")
async def channel_stats(ctx, channel: Optional[discord.TextChannel] = None):
    """Get statistics for a specific channel"""
    if channel is None:
        channel = ctx.channel

    # Ensure we have a text channel
    if not isinstance(channel, discord.TextChannel):
        await ctx.send("❌ This command only works with text channels.")
        return

    # Count messages in the last 24 hours, 7 days, and total
    now = datetime.now(timezone.utc)
    day_ago = now - timedelta(days=1)
    week_ago = now - timedelta(days=7)

    messages_24h = 0
    messages_7d = 0
    total_messages = 0

    try:
        async for message in channel.history(limit=None):
            total_messages += 1
            if message.created_at > day_ago:
                messages_24h += 1
            if message.created_at > week_ago:
                messages_7d += 1
    except discord.Forbidden:
        await ctx.send(
            "❌ I don't have permission to read message history in that channel."
        )
        return

    embed = discord.Embed(
        title=f"📊 Channel Statistics for #{channel.name}",
        color=discord.Color.green(),
        timestamp=datetime.now(),
    )

    embed.add_field(
        name="📈 Message Count",
        value=f"Last 24 hours: {messages_24h}\nLast 7 days: {messages_7d}\nTotal: {total_messages}",
        inline=True,
    )

    embed.add_field(
        name="ℹ️ Channel Info",
        value=f"Created: {channel.created_at.strftime('%B %d, %Y')}\nTopic: {channel.topic or 'None'}",
        inline=True,
    )

    await ctx.send(embed=embed)


@bot.command(name="autocleanup")
@commands.has_permissions(administrator=True)
async def setup_auto_cleanup(ctx, channel: discord.TextChannel, days: int = 7):
    """Setup automatic cleanup for a channel"""
    config["auto_cleanup"][str(channel.id)] = {
        "channel_name": channel.name,
        "days": days,
        "guild_id": ctx.guild.id,
    }
    config["cleanup_enabled"] = True
    save_config(config)

    await ctx.send(
        f"✅ Auto cleanup enabled for {channel.mention}. Messages older than {days} days will be automatically deleted."
    )

    if not auto_cleanup.is_running():
        auto_cleanup.start()


@bot.command(name="stopauto")
@commands.has_permissions(administrator=True)
async def stop_auto_cleanup(ctx, channel: Optional[discord.TextChannel] = None):
    """Stop automatic cleanup for a channel or all channels"""
    if channel:
        if str(channel.id) in config["auto_cleanup"]:
            del config["auto_cleanup"][str(channel.id)]
            await ctx.send(f"✅ Auto cleanup disabled for {channel.mention}.")
        else:
            await ctx.send(f"❌ Auto cleanup was not enabled for {channel.mention}.")
    else:
        config["auto_cleanup"] = {}
        config["cleanup_enabled"] = False
        await ctx.send("✅ Auto cleanup disabled for all channels.")
        if auto_cleanup.is_running():
            auto_cleanup.stop()

    save_config(config)


@bot.command(name="listauto")
@commands.has_permissions(manage_messages=True)
async def list_auto_cleanup(ctx):
    """List all channels with auto cleanup enabled"""
    if not config["auto_cleanup"]:
        await ctx.send("❌ No channels have auto cleanup enabled.")
        return

    embed = discord.Embed(
        title="🔄 Auto Cleanup Channels", color=discord.Color.orange()
    )

    for channel_id, settings in config["auto_cleanup"].items():
        channel = bot.get_channel(int(channel_id))
        if channel:
            embed.add_field(
                name=f"#{settings['channel_name']}",
                value=f"Cleanup after: {settings['days']} days",
                inline=False,
            )

    await ctx.send(embed=embed)


@tasks.loop(hours=24)  # Run once per day
async def auto_cleanup():
    """Automatically cleanup old messages in configured channels"""
    for channel_id, settings in config["auto_cleanup"].items():
        try:
            channel = bot.get_channel(int(channel_id))
            if not channel or not isinstance(channel, discord.TextChannel):
                continue

            cutoff_date = datetime.now(timezone.utc) - timedelta(days=settings["days"])

            def check(m):
                return m.created_at < cutoff_date

            deleted = await channel.purge(limit=None, check=check, before=cutoff_date)

            if deleted:
                logger.info(
                    f"Auto cleanup: Deleted {len(deleted)} messages from #{channel.name}"
                )

                # Log to a specific channel if configured
                log_channel_id = os.getenv("LOG_CHANNEL_ID")
                if log_channel_id:
                    log_channel = bot.get_channel(int(log_channel_id))
                    if log_channel and isinstance(log_channel, discord.TextChannel):
                        embed = discord.Embed(
                            title="🔄 Auto Cleanup Report",
                            description=f"Deleted {len(deleted)} messages older than {settings['days']} days from {channel.mention}",
                            color=discord.Color.blue(),
                            timestamp=datetime.now(),
                        )
                        await log_channel.send(embed=embed)

        except Exception as e:
            logger.error(f"Error in auto cleanup for channel {channel_id}: {e}")


# Error handling
@bot.event
async def on_command_error(ctx, error):
    """Handle command errors"""
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You don't have permission to use this command.")
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send(
            "❌ I don't have the required permissions to execute this command."
        )
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ Command not found. Use `!help` to see available commands.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("❌ Invalid argument provided. Please check the command usage.")
    else:
        await ctx.send(f"❌ An error occurred: {error}")
        logger.error(f"Unhandled error: {error}")


@clear_messages.error
@clear_all_messages.error
@clear_user_messages.error
@clear_old_messages.error
async def clear_error(ctx, error):
    """Handle errors for clear commands"""
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You need 'Manage Messages' permission to use this command.")


@setup_auto_cleanup.error
@stop_auto_cleanup.error
async def auto_cleanup_error(ctx, error):
    """Handle errors for auto cleanup commands"""
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You need 'Administrator' permission to use this command.")


if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        print("❌ No Discord token found. Please set DISCORD_TOKEN in your .env file.")
        exit(1)

    bot.run(token)
