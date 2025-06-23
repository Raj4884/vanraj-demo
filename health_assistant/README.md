# Health Assistant AI Agent

A personal health assistant that reminds you to take medications, provides health diagnoses based on symptoms, and sends voice notes and text messages to your phone.

## Features

1. **Medication Reminders**
   - Schedule medication reminders with customizable frequencies
   - Receive voice notes and text messages when it's time to take your medication
   - Manage your medication list through a user-friendly web interface

2. **Health Diagnosis**
   - Get preliminary analysis of your symptoms
   - Receive recommendations based on your health concerns
   - Important disclaimer: This is not a substitute for professional medical advice

3. **Messaging Support**
   - Receive text messages for medication reminders
   - Get voice calls with audio reminders
   - Test messaging functionality directly from the web interface

## Setup Instructions

### Prerequisites

- Python 3.7 or higher
- Twilio account for SMS and voice messaging
- Internet connection for health information retrieval

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/health-assistant.git
   cd health-assistant
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory with the following variables:
   ```
   # Twilio credentials
   TWILIO_ACCOUNT_SID=your_twilio_account_sid
   TWILIO_AUTH_TOKEN=your_twilio_auth_token
   TWILIO_PHONE_NUMBER=your_twilio_phone_number

   # User phone number
   USER_PHONE_NUMBER=your_phone_number

   # API keys for health information (if applicable)
   HEALTH_API_KEY=your_health_api_key
   ```

4. Run the application:
   ```
   python app.py
   ```

5. Open your web browser and navigate to:
   ```
   http://localhost:12000
   ```

## Usage

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

### Testing Messaging

1. Enter a test message
2. Click "Send Message"
3. Check your phone for the message

## Important Notes

- The health diagnosis feature provides general information only and should not be used as a substitute for professional medical advice.
- For serious or urgent health concerns, please contact a healthcare professional or emergency services.
- Voice messaging requires proper configuration of Twilio and publicly accessible audio files.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Twilio for messaging services
- Flask for the web framework
- Schedule for task scheduling