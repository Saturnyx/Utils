# Discord Utility Bot

A comprehensive Discord bot designed to help with server utilities including message management, automatic cleanup, and server statistics.

## Features

### 🧹 Message Management

- **Clear Messages**: Delete a specific number of recent messages
- **Clear All Messages**: Delete all messages in a channel (Admin only)
- **Clear User Messages**: Delete messages from a specific user
- **Clear Old Messages**: Delete messages older than specified days

### 🔄 Automatic Cleanup

- **Auto Cleanup**: Automatically delete old messages from specified channels
- **Configurable**: Set different cleanup periods for different channels
- **Logging**: Optional logging of cleanup activities

### 📊 Server Statistics

- **Server Stats**: Comprehensive server information including member count, channels, roles
- **Channel Stats**: Detailed statistics for specific channels including message counts

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/Saturnyx/Utils.git
   cd DiscordUtils
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**

   - Copy `.env.example` to `.env`
   - Add your Discord bot token and optional log channel ID

   ```
   DISCORD_TOKEN=your_bot_token_here
   LOG_CHANNEL_ID=your_log_channel_id_here
   ```

4. **Create a Discord Application**

   - Go to [Discord Developer Portal](https://discord.com/developers/applications)
   - Create a new application
   - Go to the "Bot" section
   - Create a bot and copy the token
   - Enable the following intents:
     - Message Content Intent
     - Server Members Intent

5. **Invite the bot to your server**
   - Go to the "OAuth2" section in your Discord application
   - Select "bot" scope
   - Select the following permissions:
     - Read Messages
     - Send Messages
     - Manage Messages
     - Read Message History
     - Embed Links

## Commands

### Message Management Commands

| Command                      | Description                                                | Permissions Required |
| ---------------------------- | ---------------------------------------------------------- | -------------------- |
| `!clear [amount]`            | Clear specified number of messages (default: 10, max: 100) | Manage Messages      |
| `!clearall`                  | Clear ALL messages in the channel (requires confirmation)  | Administrator        |
| `!clearuser <user> [amount]` | Clear messages from a specific user                        | Manage Messages      |
| `!clearold [days]`           | Clear messages older than specified days (default: 7)      | Manage Messages      |

### Statistics Commands

| Command                   | Description                            | Permissions Required |
| ------------------------- | -------------------------------------- | -------------------- |
| `!stats`                  | Show comprehensive server statistics   | None                 |
| `!channelstats [channel]` | Show statistics for a specific channel | None                 |

### Auto Cleanup Commands

| Command                         | Description                                     | Permissions Required |
| ------------------------------- | ----------------------------------------------- | -------------------- |
| `!autocleanup <channel> [days]` | Enable auto cleanup for a channel               | Administrator        |
| `!stopauto [channel]`           | Stop auto cleanup for a channel or all channels | Administrator        |
| `!listauto`                     | List all channels with auto cleanup enabled     | Manage Messages      |

## Examples

### Basic Usage

```
!clear 50                    # Delete last 50 messages
!clearuser @username 20      # Delete last 20 messages from @username
!clearold 14                 # Delete messages older than 14 days
!stats                       # Show server statistics
```

### Auto Cleanup Setup

```
!autocleanup #general 7      # Auto-delete messages older than 7 days in #general
!autocleanup #spam 1         # Auto-delete messages older than 1 day in #spam
!listauto                    # List all auto cleanup configurations
!stopauto #general           # Stop auto cleanup for #general
!stopauto                    # Stop auto cleanup for all channels
```

## Configuration

The bot creates a `bot_config.json` file to store auto cleanup settings. This file is automatically managed by the bot.

### Auto Cleanup

- Runs once every 24 hours
- Configurable per channel
- Optional logging to a designated log channel
- Preserves messages within the specified age limit

## Security Features

- **Permission Checks**: All commands require appropriate permissions
- **Confirmation Required**: Destructive operations require confirmation
- **Rate Limiting**: Built-in Discord rate limiting protection
- **Error Handling**: Comprehensive error handling and user feedback

## Logging

The bot logs important activities including:

- Message deletion operations
- Auto cleanup activities
- Errors and exceptions

Optional: Set `LOG_CHANNEL_ID` in your `.env` file to receive auto cleanup reports.

## Bot Permissions

The bot requires the following permissions:

- **Read Messages**: To see commands and channel content
- **Send Messages**: To respond to commands
- **Manage Messages**: To delete messages
- **Read Message History**: To access old messages for cleanup
- **Embed Links**: To send rich embed messages

## Troubleshooting

### Common Issues

1. **Bot doesn't respond to commands**

   - Check if the bot is online
   - Verify the bot has permission to read and send messages in the channel
   - Ensure the Message Content Intent is enabled

2. **Permission errors**

   - Verify the bot role is high enough in the server hierarchy
   - Check that required permissions are granted
   - Ensure the user has the required permissions for the command

3. **Auto cleanup not working**
   - Check if auto cleanup is enabled with `!listauto`
   - Verify the bot has Manage Messages permission in the target channels
   - Check the bot logs for error messages

### Error Messages

| Error                          | Meaning                         | Solution                                |
| ------------------------------ | ------------------------------- | --------------------------------------- |
| "You don't have permission..." | User lacks required permissions | Grant appropriate role/permissions      |
| "I don't have permission..."   | Bot lacks required permissions  | Check bot permissions in server/channel |
| "Command not found"            | Invalid command                 | Use `!help` to see available commands   |

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

If you encounter any issues or have questions:

1. Check the troubleshooting section above
2. Create an issue on GitHub
3. Join our support server (if available)

## Version History

- **v1.0.0**: Initial release with basic message management and auto cleanup features
- Features: Clear commands, auto cleanup, server statistics

---

**Note**: This bot requires Python 3.8+ and discord.py 2.3.0+
