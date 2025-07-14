#!/usr/bin/env python3
"""
Test script to validate Discord Utils Bot setup
"""

import sys
import os
from pathlib import Path


def test_imports():
    """Test if all required packages can be imported"""
    print("🔍 Testing imports...")

    try:
        import discord

        print(f"✅ discord.py version: {discord.__version__}")
    except ImportError as e:
        print(f"❌ Failed to import discord: {e}")
        return False

    try:
        from dotenv import load_dotenv

        print("✅ python-dotenv imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import dotenv: {e}")
        return False

    try:
        import json
        import asyncio
        import logging
        from datetime import datetime, timedelta, timezone

        print("✅ Standard library imports successful")
    except ImportError as e:
        print(f"❌ Failed to import standard libraries: {e}")
        return False

    return True


def test_files():
    """Test if all required files exist"""
    print("\n📁 Testing file structure...")

    required_files = [
        "main.py",
        "requirements.txt",
        ".env.example",
        "cogs/__init__.py",
        "cogs/advanced_utils.py",
        "cogs/help.py",
    ]

    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
        else:
            print(f"✅ {file_path}")

    if missing_files:
        print(f"❌ Missing files: {', '.join(missing_files)}")
        return False

    return True


def test_env_file():
    """Test environment file setup"""
    print("\n🔐 Testing environment setup...")

    env_file = Path(".env")
    env_example = Path(".env.example")

    if not env_example.exists():
        print("❌ .env.example file missing")
        return False

    print("✅ .env.example file exists")

    if not env_file.exists():
        print("⚠️ .env file not found - you'll need to create it before running the bot")
        return True

    print("✅ .env file exists")

    # Check if token is set
    try:
        from dotenv import load_dotenv

        load_dotenv()

        token = os.getenv("DISCORD_TOKEN")
        if not token or token == "your_bot_token_here":
            print("⚠️ DISCORD_TOKEN not set in .env file")
        else:
            print("✅ DISCORD_TOKEN is configured")
    except Exception as e:
        print(f"⚠️ Could not verify token: {e}")

    return True


def test_bot_syntax():
    """Test if main.py has valid syntax"""
    print("\n🐍 Testing bot syntax...")

    try:
        with open("main.py", "r", encoding="utf-8") as f:
            code = f.read()

        compile(code, "main.py", "exec")
        print("✅ main.py syntax is valid")
        return True
    except SyntaxError as e:
        print(f"❌ Syntax error in main.py: {e}")
        return False
    except UnicodeDecodeError as e:
        print(f"❌ Encoding error in main.py: {e}")
        return False
    except Exception as e:
        print(f"❌ Error reading main.py: {e}")
        return False


def main():
    """Run all tests"""
    print("🧪 Discord Utils Bot Setup Test")
    print("=" * 35)

    tests = [
        ("Import Test", test_imports),
        ("File Structure Test", test_files),
        ("Environment Test", test_env_file),
        ("Syntax Test", test_bot_syntax),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\n🔬 Running {test_name}...")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} passed")
            else:
                print(f"❌ {test_name} failed")
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")

    print("\n" + "=" * 35)
    print(f"📊 Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! Your bot setup looks good.")
        print("\n📋 Next steps:")
        print("1. Set up your .env file with your Discord bot token")
        print("2. Run 'python main.py' to start the bot")
        print("3. Test with '!help' command in Discord")
    else:
        print(
            "⚠️ Some tests failed. Please fix the issues above before running the bot."
        )

    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
