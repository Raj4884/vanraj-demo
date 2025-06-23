# Health Assistant AI Agent

A personal health assistant that reminds you to take medications, provides health diagnoses based on symptoms, and sends voice notes and text messages to your phone. This AI agent helps you stay on top of your medication schedule and provides preliminary health information when you need it.

## Features

1. **Medication Reminders**
   - Schedule medication reminders with customizable frequencies (daily, weekly, or hourly)
   - Receive voice notes and text messages when it's time to take your medication
   - Manage your medication list through a user-friendly web interface

2. **Health Diagnosis**
   - Get preliminary analysis of your symptoms
   - Receive recommendations based on your health concerns
   - Important disclaimer: This is not a substitute for professional medical advice

3. **Free Notification Support**
   - Desktop notifications on your computer
   - Email notifications via Gmail (free)
   - Browser notifications in your web interface
   - Voice reminders with local audio playback
   - In-app notification center

## How to Use

### Setup

1. Navigate to the health_assistant directory:
   ```
   cd health_assistant
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. (Optional) Configure email notifications:
   - For free email notifications, see [FREE_SETUP_GUIDE.md](health_assistant/FREE_SETUP_GUIDE.md)
   - Uses Gmail SMTP - completely free
   - Desktop and browser notifications work without any setup

4. Run the application:
   ```
   python run.py
   ```

5. Open your web browser and navigate to:
   ```
   http://localhost:12000
   ```

### Adding Medications

1. Click on "Add Medication" button
2. Fill in the medication details:
   - Name (required)
   - Dosage (optional)
   - Time (required)
   - Frequency (required)
   - Days of week (if frequency is weekly)
   - Instructions (optional)
3. Click "Save"

### Getting Health Diagnosis

1. Enter your symptoms in the text area
2. Click "Get Analysis"
3. Review the analysis results
4. Remember: This is not a substitute for professional medical advice

### Testing Notifications

1. Enter a test message
2. Click "Send Notification"
3. Check for:
   - Desktop notification popup
   - Email (if configured)
   - Browser notification
   - Console output
   - In-app notification center

## Technical Details

The Health Assistant is built using:

- **Flask**: Web framework for the user interface
- **Gmail SMTP**: For free email notifications
- **Plyer**: For cross-platform desktop notifications
- **gTTS (Google Text-to-Speech)**: For creating voice notes
- **Schedule**: For scheduling medication reminders
- **BeautifulSoup4**: For parsing health information

## Important Notes

- **Completely Free**: No monthly costs or paid services required
- The health diagnosis feature provides general information only and should not be used as a substitute for professional medical advice
- For serious or urgent health concerns, please contact a healthcare professional or emergency services
- Voice reminders are played locally on your computer
- Email notifications are optional and use Gmail's free SMTP service

## Customization

You can customize the Health Assistant by:

1. Adding more sophisticated health analysis algorithms
2. Integrating with medical APIs for more accurate diagnoses
3. Adding user authentication for multiple users
4. Implementing a mobile app interface
5. Adding support for multiple languages

## License

This project is licensed under the MIT License.