import os
from twilio.rest import Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class MessageSender:
    def __init__(self):
        # Get Twilio credentials from environment variables
        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.twilio_phone = os.getenv('TWILIO_PHONE_NUMBER')
        self.user_phone = os.getenv('USER_PHONE_NUMBER')
        
        # Initialize Twilio client if credentials are available
        if self.account_sid and self.auth_token:
            self.client = Client(self.account_sid, self.auth_token)
        else:
            self.client = None
            print("Warning: Twilio credentials not found. Messaging functionality will be limited.")
    
    def send_text_message(self, message):
        """Send a text message to the user"""
        if not self.client:
            return {"status": "error", "message": "Twilio client not initialized"}
        
        if not self.user_phone:
            return {"status": "error", "message": "User phone number not configured"}
        
        try:
            message = self.client.messages.create(
                body=message,
                from_=self.twilio_phone,
                to=self.user_phone
            )
            return {"status": "success", "message_sid": message.sid}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def send_voice_message(self, audio_file, fallback_text=None):
        """Send a voice message to the user"""
        if not self.client:
            return {"status": "error", "message": "Twilio client not initialized"}
        
        if not self.user_phone:
            return {"status": "error", "message": "User phone number not configured"}
        
        if not os.path.exists(audio_file):
            return {"status": "error", "message": f"Audio file not found: {audio_file}"}
        
        try:
            # Get the absolute URL for the audio file
            # In a real application, you would host this file on a publicly accessible server
            # For demonstration, we'll use a placeholder URL
            audio_url = f"https://example.com/audio/{os.path.basename(audio_file)}"
            
            # Create a call with TwiML to play the audio
            call = self.client.calls.create(
                twiml=f'<Response><Play>{audio_url}</Play><Say>{fallback_text or "Medication reminder"}</Say></Response>',
                from_=self.twilio_phone,
                to=self.user_phone
            )
            return {"status": "success", "call_sid": call.sid}
        except Exception as e:
            return {"status": "error", "message": str(e)}