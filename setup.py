#!/usr/bin/env python3
"""
Discord Utils Bot Setup Script
This script helps you set up the Discord bot quickly.
"""

import os
import subprocess
import sys
from pathlib import Path


def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required!")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version}")
    return True


def install_requirements():
    """Install required packages"""
    print("\n🔄 Installing required packages...")
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
        )
        print("✅ All packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install packages: {e}")
        return False


def create_env_file():
    """Create .env file from template"""
    print("\n🔧 Setting up environment file...")

    env_example = Path(".env.example")
    env_file = Path(".env")

    if not env_example.exists():
        print("❌ .env.example file not found!")
        return False

    if env_file.exists():
        overwrite = input("📁 .env file already exists. Overwrite? (y/N): ")
        if overwrite.lower() != "y":
            print("⏭️ Skipping .env file creation.")
            return True

    with open(env_example, "r") as f:
        content = f.read()

    print("\n🔑 Please provide your Discord bot configuration:")

    token = input("Enter your Discord bot token: ").strip()
    if not token:
        print("❌ Bot token is required!")
        return False

    content = content.replace("your_bot_token_here", token)

    log_channel = input(
        "Enter log channel ID (optional, press Enter to skip): "
    ).strip()
    if log_channel:
        content = content.replace("your_log_channel_id_here", log_channel)

    with open(env_file, "w") as f:
        f.write(content)

    print("✅ .env file created successfully!")
    return True


def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")

    directories = ["logs", "backups"]

    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created directory: {directory}")

    return True


def display_setup_instructions():
    """Display final setup instructions"""
    print("\n" + "=" * 50)
    print("🎉 SETUP COMPLETE!")
    print("=" * 50)
    print("\n📋 Next steps:")
    print("1. Make sure your Discord bot has the following permissions:")
    print("   - Read Messages")
    print("   - Send Messages")
    print("   - Manage Messages")
    print("   - Read Message History")
    print("   - Embed Links")
    print("\n2. Enable the following intents in Discord Developer Portal:")
    print("   - Message Content Intent")
    print("   - Server Members Intent")
    print("\n3. Run the bot:")
    print("   python main.py")
    print("\n4. Test with basic commands:")
    print("   !help - Show help menu")
    print("   !stats - Show server statistics")
    print("   !clear 5 - Clear 5 messages")
    print("\n📖 For more information, check README.md")
    print("\n🐛 If you encounter issues:")
    print("   - Check the troubleshooting section in README.md")
    print("   - Ensure all permissions are correctly set")
    print("   - Check bot logs for error messages")


def main():
    """Main setup function"""
    print("🤖 Discord Utils Bot Setup")
    print("=" * 30)

    # --- Check Python version
    if not check_python_version():
        return False

    # --- Install requirements
    if not install_requirements():
        return False

    # --- Create .env file
    if not create_env_file():
        return False

    # --- Create directories
    if not create_directories():
        return False

    # --- Display final instructions
    display_setup_instructions()

    return True


if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n✅ Setup completed successfully!")
        else:
            print("\n❌ Setup failed. Please check the errors above.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠️ Setup cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error during setup: {e}")
        sys.exit(1)
