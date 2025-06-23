# Free Health Assistant Setup Guide

This guide shows you how to set up the Health Assistant using completely free resources instead of paid services like Twilio.

## Free Notification Methods

The Health Assistant now supports multiple free notification methods:

1. **Desktop Notifications** - Pop-up notifications on your computer
2. **Email Notifications** - Free email alerts using Gmail SMTP
3. **Browser Notifications** - Web-based notifications in your browser
4. **Console Output** - Terminal/console messages
5. **Web Interface Notifications** - In-app notification center

## Setup Instructions

### 1. Install Dependencies

```bash
cd health_assistant
pip install -r requirements.txt
```

### 2. Configure Email Notifications (Optional but Recommended)

To enable email notifications, you'll need a Gmail account:

1. **Enable 2-Factor Authentication** on your Gmail account
2. **Generate an App Password**:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate a password for "Mail"
   - Copy the 16-character password

3. **Configure Environment Variables**:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` file:
   ```
   EMAIL_ADDRESS=your_email@gmail.com
   EMAIL_PASSWORD=your_16_character_app_password
   RECIPIENT_EMAIL=recipient@gmail.com
   
   ENABLE_DESKTOP_NOTIFICATIONS=true
   ENABLE_EMAIL_NOTIFICATIONS=true
   ENABLE_BROWSER_NOTIFICATIONS=true
   ```

### 3. Run the Application

```bash
python run.py
```

The application will be available at `http://localhost:12000`

## How It Works

### Desktop Notifications
- Uses the `plyer` library for cross-platform desktop notifications
- Works on Windows, macOS, and Linux
- No setup required - works out of the box

### Email Notifications
- Uses Gmail's free SMTP service
- Sends formatted email reminders
- Can include audio attachments for voice reminders
- Completely free with any Gmail account

### Browser Notifications
- Uses the Web Notifications API
- Stores notifications in the web interface
- Shows unread notification count
- Works in all modern browsers

### Voice Reminders
- Creates audio files using Google Text-to-Speech (gTTS)
- Plays audio locally on your computer
- Can send audio files via email
- No external API costs

## Features

### Medication Reminders
- Schedule medications with custom frequencies
- Get notifications via multiple channels
- Voice and text reminders
- Automatic scheduling

### Health Diagnosis
- Symptom analysis using free health databases
- Preliminary health recommendations
- Emergency situation detection
- Educational health information

### Notification Center
- View all recent notifications
- Mark notifications as read
- Auto-refresh every 30 seconds
- Clean, organized interface

## Cost Breakdown

| Feature | Cost | Notes |
|---------|------|-------|
| Desktop Notifications | Free | Built into OS |
| Email Notifications | Free | Gmail SMTP |
| Browser Notifications | Free | Web API |
| Voice Generation | Free | Google TTS |
| Web Interface | Free | Local hosting |
| Health Information | Free | Public databases |

**Total Cost: $0/month** 🎉

## Troubleshooting

### Desktop Notifications Not Working
- Check if notifications are enabled in your OS settings
- Some Linux distributions may need additional packages

### Email Not Sending
- Verify Gmail app password is correct
- Check that 2FA is enabled on your Google account
- Ensure "Less secure app access" is disabled (use app passwords instead)

### Browser Notifications Not Showing
- Click "Allow" when prompted for notification permission
- Check browser notification settings
- Some browsers block notifications on localhost

### Audio Not Playing
- Check system audio settings
- Verify audio drivers are installed
- Try different audio formats if needed

## Advanced Configuration

### Custom Notification Sounds
Place custom audio files in the `audio/` directory and reference them in your medication settings.

### Email Templates
Modify the email templates in `messaging/message_sender.py` to customize the appearance of email notifications.

### Notification Frequency
Adjust the auto-refresh interval in `static/js/script.js` (currently set to 30 seconds).

## Security Notes

- App passwords are more secure than using your main Gmail password
- All data is stored locally on your computer
- No data is sent to external services except Gmail for email notifications
- Audio files are generated and stored locally

## Support

If you encounter any issues:
1. Check the console output for error messages
2. Verify all dependencies are installed correctly
3. Ensure your `.env` file is configured properly
4. Test each notification method individually

This free setup provides all the functionality of paid services without any monthly costs!