import discord
from discord.ext import commands


class Help(commands.Cog):
    """Custom help command for the Discord Utils Bot"""

    def __init__(self, bot):
        self.bot = bot
        bot.remove_command("help")

    @commands.command(name="help")
    async def custom_help(self, ctx, *, command_name: str = None):
        """Show help information for commands"""

        if command_name:

            cmd = self.bot.get_command(command_name.lower())
            if not cmd:
                await ctx.send(f"❌ Command `{command_name}` not found.")
                return

            embed = discord.Embed(
                title=f"📖 Help: {cmd.name}",
                description=cmd.help or "No description available.",
                color=discord.Color.blue(),
            )

            if cmd.usage:
                embed.add_field(
                    name="Usage", value=f"`!{cmd.name} {cmd.usage}`", inline=False
                )
            else:
                embed.add_field(name="Usage", value=f"`!{cmd.name}`", inline=False)

            if hasattr(cmd, "checks") and cmd.checks:
                perms = []
                for check in cmd.checks:
                    if hasattr(check, "__name__"):
                        if "administrator" in check.__name__:
                            perms.append("Administrator")
                        elif "manage_messages" in check.__name__:
                            perms.append("Manage Messages")
                        elif "manage_channels" in check.__name__:
                            perms.append("Manage Channels")

                if perms:
                    embed.add_field(
                        name="Required Permissions",
                        value=", ".join(perms),
                        inline=False,
                    )

            await ctx.send(embed=embed)
            return

        embed = discord.Embed(
            title="🤖 Discord Utils Bot - Help",
            description="A comprehensive utility bot for Discord server management.",
            color=discord.Color.blue(),
        )

        cleanup_commands = [
            ("clear [amount]", "Clear specified number of messages (default: 10)"),
            ("clearall", "Clear ALL messages in channel (requires confirmation)"),
            ("clearuser <user> [amount]", "Clear messages from a specific user"),
            ("clearold [days]", "Clear messages older than specified days"),
        ]

        cleanup_text = "\n".join(
            [f"`!{cmd}` - {desc}" for cmd, desc in cleanup_commands]
        )
        embed.add_field(name="🧹 Message Management", value=cleanup_text, inline=False)

        stats_commands = [
            ("stats", "Show comprehensive server statistics"),
            ("channelstats [channel]", "Show statistics for a specific channel"),
            ("membercount", "Get detailed member count breakdown"),
            ("userinfo [user]", "Get detailed information about a user"),
            ("roleinfo <role_name>", "Get information about a specific role"),
        ]

        stats_text = "\n".join([f"`!{cmd}` - {desc}" for cmd, desc in stats_commands])
        embed.add_field(name="📊 Statistics", value=stats_text, inline=False)

        auto_commands = [
            ("autocleanup <channel> [days]", "Enable auto cleanup for a channel"),
            ("stopauto [channel]", "Stop auto cleanup for a channel"),
            ("listauto", "List all channels with auto cleanup enabled"),
        ]

        auto_text = "\n".join([f"`!{cmd}` - {desc}" for cmd, desc in auto_commands])
        embed.add_field(name="🔄 Auto Cleanup", value=auto_text, inline=False)

        util_commands = [
            ("backup <channel> [limit]", "Create a backup of channel messages"),
            ("slowmode [seconds]", "Set slowmode for the current channel"),
        ]

        util_text = "\n".join([f"`!{cmd}` - {desc}" for cmd, desc in util_commands])
        embed.add_field(name="🛠️ Utilities", value=util_text, inline=False)

        embed.add_field(
            name="💡 Tips",
            value="• Use `!help <command>` for detailed help on a specific command\n"
            "• Commands in `<>` are required, commands in `[]` are optional\n"
            "• Most commands require specific permissions",
            inline=False,
        )

        embed.set_footer(text="Discord Utils Bot | Use responsibly!")

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Help(bot))
