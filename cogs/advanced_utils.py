import discord
from discord.ext import commands
import asyncio
from datetime import datetime, timezone

class AdvancedUtils(commands.Cog):
    """Advanced utility commands for Discord server management"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='backup')
    @commands.has_permissions(administrator=True)
    async def backup_channel(self, ctx, channel: discord.TextChannel = None, limit: int = 1000):
        """Create a backup of channel messages"""
        if channel is None:
            channel = ctx.channel
        
        if limit > 5000:
            await ctx.send("❌ Limit cannot exceed 5000 messages for performance reasons.")
            return
        
        await ctx.send(f"🔄 Creating backup of {channel.mention}... This may take a while.")
        
        messages = []
        try:
            async for message in channel.history(limit=limit):
                messages.append({
                    'author': str(message.author),
                    'content': message.content,
                    'timestamp': message.created_at.isoformat(),
                    'attachments': [att.url for att in message.attachments],
                    'embeds': len(message.embeds)
                })
        except discord.Forbidden:
            await ctx.send("❌ I don't have permission to read message history in that channel.")
            return
        
        # Create a simple text backup
        backup_content = f"Channel Backup: #{channel.name}\n"
        backup_content += f"Generated: {datetime.now(timezone.utc).isoformat()}\n"
        backup_content += f"Total Messages: {len(messages)}\n"
        backup_content += "="*50 + "\n\n"
        
        for msg in reversed(messages):
            backup_content += f"[{msg['timestamp']}] {msg['author']}: {msg['content']}\n"
            if msg['attachments']:
                backup_content += f"  Attachments: {', '.join(msg['attachments'])}\n"
            backup_content += "\n"
        
        # Save to file and send
        filename = f"backup_{channel.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(backup_content)
            
            await ctx.send(f"✅ Backup created successfully! {len(messages)} messages backed up.", 
                          file=discord.File(filename))
            
            # Clean up the file
            import os
            os.remove(filename)
            
        except Exception as e:
            await ctx.send(f"❌ Error creating backup: {e}")
    
    @commands.command(name='membercount')
    async def member_count(self, ctx):
        """Get detailed member count breakdown"""
        guild = ctx.guild
        
        # Count members by status
        online = len([m for m in guild.members if m.status == discord.Status.online])
        idle = len([m for m in guild.members if m.status == discord.Status.idle])
        dnd = len([m for m in guild.members if m.status == discord.Status.dnd])
        offline = len([m for m in guild.members if m.status == discord.Status.offline])
        
        # Count bots vs humans
        bots = len([m for m in guild.members if m.bot])
        humans = guild.member_count - bots
        
        embed = discord.Embed(
            title=f"👥 Member Count for {guild.name}",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="📊 Total Members",
            value=f"**{guild.member_count}**",
            inline=True
        )
        
        embed.add_field(
            name="👤 Humans vs Bots",
            value=f"Humans: {humans}\nBots: {bots}",
            inline=True
        )
        
        embed.add_field(
            name="🟢 Status Breakdown",
            value=f"Online: {online}\nIdle: {idle}\nDND: {dnd}\nOffline: {offline}",
            inline=True
        )
        
        await ctx.send(embed=embed)
    
    @commands.command(name='roleinfo')
    async def role_info(self, ctx, *, role_name: str):
        """Get information about a specific role"""
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        
        if not role:
            await ctx.send(f"❌ Role '{role_name}' not found.")
            return
        
        embed = discord.Embed(
            title=f"🎭 Role Information: {role.name}",
            color=role.color if role.color != discord.Color.default() else discord.Color.blue()
        )
        
        embed.add_field(
            name="👥 Members",
            value=str(len(role.members)),
            inline=True
        )
        
        embed.add_field(
            name="📅 Created",
            value=role.created_at.strftime('%B %d, %Y'),
            inline=True
        )
        
        embed.add_field(
            name="🎨 Color",
            value=f"#{role.color.value:06x}" if role.color != discord.Color.default() else "Default",
            inline=True
        )
        
        embed.add_field(
            name="📍 Position",
            value=str(role.position),
            inline=True
        )
        
        embed.add_field(
            name="🔒 Hoisted",
            value="Yes" if role.hoist else "No",
            inline=True
        )
        
        embed.add_field(
            name="📢 Mentionable",
            value="Yes" if role.mentionable else "No",
            inline=True
        )
        
        # List some members if the role has few members
        if len(role.members) <= 10:
            member_list = "\n".join([member.display_name for member in role.members])
            embed.add_field(
                name="👤 Members",
                value=member_list if member_list else "None",
                inline=False
            )
        
        await ctx.send(embed=embed)
    
    @commands.command(name='slowmode')
    @commands.has_permissions(manage_channels=True)
    async def set_slowmode(self, ctx, seconds: int = 0):
        """Set slowmode for the current channel"""
        if seconds < 0 or seconds > 21600:  # Max 6 hours
            await ctx.send("❌ Slowmode must be between 0 and 21600 seconds (6 hours).")
            return
        
        try:
            await ctx.channel.edit(slowmode_delay=seconds)
            
            if seconds == 0:
                await ctx.send("✅ Slowmode disabled.")
            else:
                minutes, secs = divmod(seconds, 60)
                hours, minutes = divmod(minutes, 60)
                
                time_str = ""
                if hours:
                    time_str += f"{hours}h "
                if minutes:
                    time_str += f"{minutes}m "
                if secs:
                    time_str += f"{secs}s"
                
                await ctx.send(f"✅ Slowmode set to {time_str.strip()}.")
        
        except discord.Forbidden:
            await ctx.send("❌ I don't have permission to manage this channel.")
        except Exception as e:
            await ctx.send(f"❌ Error setting slowmode: {e}")
    
    @commands.command(name='userinfo')
    async def user_info(self, ctx, user: discord.Member = None):
        """Get detailed information about a user"""
        if user is None:
            user = ctx.author
        
        embed = discord.Embed(
            title=f"👤 User Information: {user.display_name}",
            color=user.color
        )
        
        embed.set_thumbnail(url=user.avatar.url if user.avatar else user.default_avatar.url)
        
        embed.add_field(
            name="🏷️ Username",
            value=f"{user.name}#{user.discriminator}",
            inline=True
        )
        
        embed.add_field(
            name="🆔 User ID",
            value=str(user.id),
            inline=True
        )
        
        embed.add_field(
            name="📅 Account Created",
            value=user.created_at.strftime('%B %d, %Y'),
            inline=True
        )
        
        embed.add_field(
            name="📅 Joined Server",
            value=user.joined_at.strftime('%B %d, %Y') if user.joined_at else "Unknown",
            inline=True
        )
        
        embed.add_field(
            name="🤖 Bot",
            value="Yes" if user.bot else "No",
            inline=True
        )
        
        embed.add_field(
            name="🎭 Roles",
            value=f"{len(user.roles) - 1} roles",  # -1 to exclude @everyone
            inline=True
        )
        
        # List roles if not too many
        if len(user.roles) <= 15:
            role_list = ", ".join([role.name for role in user.roles[1:]])  # Skip @everyone
            if role_list:
                embed.add_field(
                    name="🎭 Role List",
                    value=role_list,
                    inline=False
                )
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(AdvancedUtils(bot))
