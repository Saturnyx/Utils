# Contributing to Discord Utils Bot

Thank you for your interest in contributing to the Discord Utils Bot! This guide will help you get started with contributing to this project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Code Style Guidelines](#code-style-guidelines)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Reporting Issues](#reporting-issues)

## Code of Conduct

This project adheres to a [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Discord bot token
- Basic understanding of Discord.py library
- Git for version control

### Development Setup

1. **Fork the repository**

   ```bash
   # Fork the repo on GitHub, then clone your fork
   git clone https://github.com/YOUR_USERNAME/Utils.git
   cd Utils
   ```

2. **Set up the development environment**

   ```bash
   # Run the setup script
   python setup.py
   ```

3. **Create environment variables**

   ```bash
   # Copy the example environment file
   cp .env.example .env
   # Edit .env with your Discord bot token and other settings
   ```

4. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

5. **Test the installation**
   ```bash
   python test_setup.py
   ```

## How to Contribute

### Types of Contributions

We welcome several types of contributions:

- **Bug fixes**: Fix issues in existing functionality
- **Feature enhancements**: Improve existing features
- **New features**: Add new utilities or commands
- **Documentation**: Improve README, code comments, or guides
- **Testing**: Add or improve test coverage
- **Code optimization**: Performance improvements and refactoring

### Development Process

1. **Create a new branch**

   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/issue-description
   ```

2. **Make your changes**

   - Follow the code style guidelines below
   - Add appropriate comments and documentation
   - Test your changes thoroughly

3. **Commit your changes**

   ```bash
   git add .
   git commit -m "Add descriptive commit message"
   ```

4. **Push to your fork**

   ```bash
   git push origin feature/your-feature-name
   ```

5. **Create a Pull Request**
   - Go to the original repository on GitHub
   - Click "New Pull Request"
   - Provide a clear description of your changes

## Code Style Guidelines

### Python Code Style

- Follow PEP 8 style guidelines
- Use descriptive variable and function names
- Add docstrings to all functions and classes
- Keep line length under 88 characters (Black formatter standard)
- Use type hints where appropriate

### Example:

```python
from typing import Optional
import discord
from discord.ext import commands

async def clear_messages(
    ctx: commands.Context,
    amount: int,
    user: Optional[discord.Member] = None
) -> None:
    """
    Clear messages from a channel.

    Args:
        ctx: The command context
        amount: Number of messages to delete
        user: Optional user to filter messages by
    """
    # Implementation here
    pass
```

### Discord Bot Specific Guidelines

- Always check for proper permissions before executing commands
- Include error handling for Discord API rate limits
- Use embed messages for better formatting when appropriate
- Log important actions for debugging purposes
- Follow Discord's best practices for bot development

### File Organization

- **main.py**: Core bot setup and event handlers
- **cogs/**: Modular command groups
  - **advanced_utils.py**: Advanced utility commands
  - **help.py**: Help and information commands
- **setup.py**: Installation and setup script
- **test_setup.py**: Setup validation tests

## Testing

### Running Tests

```bash
# Run the setup test
python test_setup.py

# Test bot functionality (requires valid Discord token)
python main.py
```

### Testing Guidelines

- Test all new commands thoroughly
- Verify permissions work correctly
- Test error handling scenarios
- Check rate limiting behavior
- Validate all user inputs

### Manual Testing Checklist

- [ ] Command responds correctly
- [ ] Proper permission checks
- [ ] Error messages are helpful
- [ ] Rate limiting works
- [ ] Logging functions properly

## Submitting Changes

### Pull Request Guidelines

1. **Title**: Use a clear, descriptive title
2. **Description**: Explain what changes you made and why
3. **Testing**: Describe how you tested your changes
4. **Screenshots**: Include screenshots for UI changes
5. **Breaking Changes**: Clearly mark any breaking changes

### Pull Request Template

```markdown
## Description

Brief description of changes

## Type of Change

- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring

## Testing

- [ ] Tested manually
- [ ] Added/updated tests
- [ ] All existing tests pass

## Screenshots (if applicable)

Add screenshots here

## Additional Notes

Any additional information
```

## Reporting Issues

### Bug Reports

When reporting bugs, please include:

- **Description**: Clear description of the issue
- **Steps to Reproduce**: Detailed steps to reproduce the bug
- **Expected Behavior**: What you expected to happen
- **Actual Behavior**: What actually happened
- **Environment**: Python version, Discord.py version, OS
- **Logs**: Relevant error messages or logs

### Feature Requests

When requesting features, please include:

- **Description**: Clear description of the feature
- **Use Case**: Why this feature would be useful
- **Implementation Ideas**: Any thoughts on how it could be implemented
- **Alternatives**: Any alternative solutions you've considered

## Development Tips

### Common Commands

```bash
# Format code with Black
black .

# Check code style with flake8
flake8 .

# Sort imports with isort
isort .

# Run the bot in development mode
python main.py
```

### Useful Resources

- [Discord.py Documentation](https://discordpy.readthedocs.io/)
- [Discord Developer Portal](https://discord.com/developers/applications)
- [Python Style Guide (PEP 8)](https://pep8.org/)
- [Git Documentation](https://git-scm.com/doc)

## Questions?

If you have questions about contributing, feel free to:

- Open an issue with the "question" label
- Join our Discord server (if available)
- Contact the maintainers directly

## Recognition

Contributors will be recognized in:

- The project README
- Release notes for significant contributions
- Special thanks in documentation updates

Thank you for contributing to Discord Utils Bot! 🎉
