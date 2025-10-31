# Instagram Comment Bot

A Python bot that continuously posts comments on a specified Instagram post.

## ⚠️ CRITICAL WARNINGS

- **This bot may violate Instagram's Terms of Service**
- **Your account may be temporarily or permanently banned**
- **Use a secondary/test account, NEVER your main account**
- **Instagram actively detects and blocks bot behavior**
- **This is for educational purposes only**

## Features

- 🔄 Continuous commenting with configurable delays
- 🎲 Random comment selection from a pool
- 💾 Session persistence (stays logged in)
- 📝 Detailed logging to file and console
- ⏱️ Rate limiting to reduce detection
- 🛡️ Error handling and automatic recovery
- 🔐 Secure credential management via .env file

## Setup

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure the Bot

Edit `config.env` and set:

```env
# Your Instagram credentials (use a test account!)
INSTAGRAM_USERNAME=your_username_here
INSTAGRAM_PASSWORD=your_password_here

# Instagram post URL to comment on
POST_URL=https://www.instagram.com/p/EXAMPLE/

# Delay between comments (seconds)
# Recommended: 300-600 (5-10 minutes) minimum
MIN_DELAY=300
MAX_DELAY=600

# Comments (comma-separated)
COMMENTS=Great post!,Love this!,Amazing content!
```

### 3. Run the Bot

```bash
python instagram_bot.py
```

## Configuration Tips

### Delays
- **Minimum recommended: 5-10 minutes (300-600 seconds)**
- Shorter delays = higher risk of detection
- Longer delays = safer but slower

### Comments
- Use varied, natural-sounding comments
- Avoid spam-like repetitive text
- Mix short and long comments
- Add emojis for variety (optional)

Example:
```
COMMENTS=Love this! 😍,Great content!,This is amazing,Keep up the good work,Inspiring! ✨,Wow! 🔥,Beautiful post,So creative!
```

## Running in Background

### On macOS/Linux:

```bash
# Run in background
nohup python instagram_bot.py &

# Check if running
ps aux | grep instagram_bot

# View logs in real-time
tail -f instagram_bot.log

# Stop the bot
pkill -f instagram_bot.py
```

### Using screen (recommended for long sessions):

```bash
# Start a new screen session
screen -S instagram_bot

# Run the bot
python instagram_bot.py

# Detach: Press Ctrl+A, then D

# Reattach later
screen -r instagram_bot

# Kill session
screen -X -S instagram_bot quit
```

## Files Created

- `session.json` - Stores login session (keeps you logged in)
- `instagram_bot.log` - Detailed log of all bot activities

## Troubleshooting

### "Challenge Required" Error
- Instagram needs verification
- Login manually through the app first
- Complete any verification steps
- Wait a few hours before trying again

### "Feedback Required" Error
- You've been rate limited or flagged
- Stop the bot immediately
- Wait 24-48 hours
- Increase delays in config.env

### Bot Stops Commenting
- Check `instagram_bot.log` for errors
- Verify account isn't banned (try logging in manually)
- Increase delays between comments
- Use more varied comments

## Best Practices

1. **Use a test account** - Never risk your main account
2. **Start slowly** - Use longer delays at first (10-15 minutes)
3. **Monitor logs** - Check for warnings or rate limiting
4. **Vary comments** - Use 10-20 different comment variations
5. **Don't run 24/7** - Take breaks (run 2-3 hours, pause, repeat)
6. **Stop if flagged** - If you get warnings, stop immediately

## Legal & Ethical Considerations

This bot is provided for **educational purposes only**. By using this bot:

- You acknowledge the risks of account suspension/ban
- You agree not to use it for spam or harassment
- You take full responsibility for any consequences
- You understand this may violate Instagram's Terms of Service

## Stopping the Bot

Press `Ctrl+C` in the terminal to stop gracefully.

The bot will show total comments posted and runtime.

## Support

If you encounter issues:
1. Check `instagram_bot.log` for detailed errors
2. Verify your credentials are correct in `config.env`
3. Ensure the post URL is valid and public
4. Try increasing delays to avoid rate limits

