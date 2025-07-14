# Discord Utils Bot - Quick Start Guide

## 🎯 What This Bot Does

This Discord utility bot provides comprehensive server management features:

### 🧹 **Message Management**

- **`!clear [amount]`** - Delete recent messages (default: 10, max: 100)
- **`!clearall`** - Delete ALL messages in a channel (Admin only, requires confirmation)
- **`!clearuser <@user> [amount]`** - Delete messages from a specific user
- **`!clearold [days]`** - Delete messages older than specified days

### 🔄 **Automatic Cleanup**

- **`!autocleanup <#channel> [days]`** - Auto-delete old messages (default: 7 days)
- **`!stopauto [#channel]`** - Stop auto cleanup for channel or all channels
- **`!listauto`** - List channels with auto cleanup enabled

### 📊 **Server Statistics**

- **`!stats`** - Comprehensive server statistics
- **`!channelstats [#channel]`** - Detailed channel statistics
- **`!membercount`** - Member count breakdown by status
- **`!userinfo [@user]`** - Detailed user information
- **`!roleinfo <role_name>`** - Role information and members

### 🛠️ **Utilities**

- **`!backup <#channel> [limit]`** - Create message backup file
- **`!slowmode [seconds]`** - Set channel slowmode (0-21600 seconds)
- **`!help [command]`** - Show help for all commands or specific command

## 🚀 Quick Setup

### 1. **Install Dependencies**

```bash
# Option 1: Run setup script
python setup.py

# Option 2: Manual installation
pip install -r requirements.txt
```

### 2. **Configure Discord Bot**

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create new application → Bot section → Create bot
3. Copy the bot token
4. Enable these intents:
   - ✅ Message Content Intent
   - ✅ Server Members Intent

### 3. **Set Up Environment**

```bash
# Copy example file
cp .env.example .env

# Edit .env file and add your token
DISCORD_TOKEN=your_bot_token_here
LOG_CHANNEL_ID=your_log_channel_id_here  # Optional
```

### 4. **Invite Bot to Server**

Required permissions:

- ✅ Read Messages
- ✅ Send Messages
- ✅ Manage Messages
- ✅ Read Message History
- ✅ Embed Links

### 5. **Run the Bot**

```bash
# Windows
run.bat

# Or manually
python main.py
```

## 🔒 Security & Permissions

### **Command Permissions**

- **Manage Messages**: `clear`, `clearuser`, `clearold`, `listauto`
- **Administrator**: `clearall`, `autocleanup`, `stopauto`
- **Manage Channels**: `slowmode`
- **No permissions required**: `stats`, `channelstats`, `help`, `userinfo`, `roleinfo`

### **Safety Features**

- ✅ Confirmation required for destructive operations
- ✅ Rate limiting protection
- ✅ Permission validation
- ✅ Error handling and user feedback
- ✅ Auto cleanup logging

## 📋 Examples

```bash
# Basic message management
!clear 20                    # Delete last 20 messages
!clearuser @spammer 50       # Delete 50 messages from @spammer
!clearold 14                 # Delete messages older than 2 weeks

# Auto cleanup setup
!autocleanup #general 7      # Auto cleanup #general every 7 days
!autocleanup #spam 1         # Auto cleanup #spam daily
!listauto                    # See all auto cleanup configs

# Server information
!stats                       # Full server statistics
!channelstats #general       # Statistics for #general
!userinfo @username          # Info about @username

# Utilities
!backup #important 1000      # Backup last 1000 messages from #important
!slowmode 30                 # Set 30 second slowmode
!slowmode 0                  # Disable slowmode
```

## 🐛 Troubleshooting

### **Bot not responding?**

1. Check bot is online and has proper permissions
2. Verify Message Content Intent is enabled
3. Ensure bot role is high enough in hierarchy

### **Permission errors?**

1. Bot needs "Manage Messages" for cleanup commands
2. User needs appropriate permissions for command
3. Check bot role position vs target role position

### **Auto cleanup not working?**

1. Verify setup with `!listauto`
2. Check bot has permissions in target channels
3. Review logs for error messages

## 📁 File Structure

```
DiscordUtils/
├── main.py              # Main bot file
├── requirements.txt     # Dependencies
├── setup.py            # Setup script
├── test_setup.py       # Validation script
├── run.bat             # Windows launcher
├── .env.example        # Environment template
├── .env                # Your configuration (create this)
├── cogs/
│   ├── __init__.py
│   ├── advanced_utils.py  # Advanced utility commands
│   └── help.py           # Custom help system
└── bot_config.json     # Auto-generated bot config
```

## 🔧 Advanced Configuration

### **Auto Cleanup Logging**

Set `LOG_CHANNEL_ID` in `.env` to receive auto cleanup reports.

### **Custom Cleanup Schedules**

Modify the `@tasks.loop(hours=24)` decorator in `main.py` to change frequency.

### **Adding Custom Commands**

Create new cogs in the `cogs/` directory and load them in `main.py`.

---

**Need help?** Use `!help` in Discord or check the full README.md file.
