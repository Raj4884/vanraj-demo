import os
import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.audio import MIMEAudio
from dotenv import load_dotenv
from plyer import notification
import threading
import time

# Load environment variables
load_dotenv()

class MessageSender:
    def __init__(self):
        # Get email credentials from environment variables
        self.email_address = os.getenv('EMAIL_ADDRESS')
        self.email_password = os.getenv('EMAIL_PASSWORD')
        self.recipient_email = os.getenv('RECIPIENT_EMAIL')
        
        # Notification settings
        self.enable_desktop = os.getenv('ENABLE_DESKTOP_NOTIFICATIONS', 'true').lower() == 'true'
        self.enable_email = os.getenv('ENABLE_EMAIL_NOTIFICATIONS', 'true').lower() == 'true'
        self.enable_browser = os.getenv('ENABLE_BROWSER_NOTIFICATIONS', 'true').lower() == 'true'
        
        # Store notifications for web interface
        self.notifications_file = 'data/notifications.json'
        os.makedirs('data', exist_ok=True)
    
    def send_text_message(self, message):
        """Send a notification using multiple free methods"""
        results = []
        
        # Desktop notification
        if self.enable_desktop:
            try:
                notification.notify(
                    title="Health Assistant Reminder",
                    message=message,
                    timeout=10
                )
                results.append({"method": "desktop", "status": "success"})
            except Exception as e:
                results.append({"method": "desktop", "status": "error", "message": str(e)})
        
        # Email notification
        if self.enable_email and self.email_address and self.recipient_email:
            email_result = self._send_email(message)
            results.append({"method": "email", **email_result})
        
        # Browser notification (store for web interface)
        if self.enable_browser:
            browser_result = self._store_browser_notification(message)
            results.append({"method": "browser", **browser_result})
        
        # Console notification (always available)
        print(f"🔔 HEALTH REMINDER: {message}")
        results.append({"method": "console", "status": "success"})
        
        return {"status": "success", "results": results}
    
    def send_voice_message(self, audio_file, fallback_text=None):
        """Send a voice notification using available methods"""
        results = []
        
        # Play audio file locally if it exists
        if os.path.exists(audio_file):
            try:
                # Try to play the audio file using system commands
                if os.name == 'nt':  # Windows
                    os.system(f'start {audio_file}')
                elif os.name == 'posix':  # Linux/Mac
                    os.system(f'afplay {audio_file} || aplay {audio_file} || paplay {audio_file}')
                results.append({"method": "local_audio", "status": "success"})
            except Exception as e:
                results.append({"method": "local_audio", "status": "error", "message": str(e)})
        
        # Send email with audio attachment
        if self.enable_email and self.email_address and self.recipient_email and os.path.exists(audio_file):
            email_result = self._send_email_with_audio(fallback_text or "Voice reminder", audio_file)
            results.append({"method": "email_audio", **email_result})
        
        # Fallback to text notification
        if fallback_text:
            text_result = self.send_text_message(fallback_text)
            results.append({"method": "text_fallback", **text_result})
        
        return {"status": "success", "results": results}
    
    def _send_email(self, message, subject="Health Assistant Reminder"):
        """Send email notification using Gmail SMTP"""
        if not self.email_address or not self.email_password or not self.recipient_email:
            return {"status": "error", "message": "Email credentials not configured"}
        
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.email_address
            msg['To'] = self.recipient_email
            msg['Subject'] = subject
            
            # Email body
            body = f"""
            Health Assistant Reminder
            
            {message}
            
            Time: {time.strftime('%Y-%m-%d %H:%M:%S')}
            
            This is an automated reminder from your Health Assistant.
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Gmail SMTP configuration
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.email_address, self.email_password)
            
            # Send email
            text = msg.as_string()
            server.sendmail(self.email_address, self.recipient_email, text)
            server.quit()
            
            return {"status": "success", "message": "Email sent successfully"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def _send_email_with_audio(self, message, audio_file):
        """Send email with audio attachment"""
        if not self.email_address or not self.email_password or not self.recipient_email:
            return {"status": "error", "message": "Email credentials not configured"}
        
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.email_address
            msg['To'] = self.recipient_email
            msg['Subject'] = "Health Assistant Voice Reminder"
            
            # Email body
            body = f"""
            Health Assistant Voice Reminder
            
            {message}
            
            Please find the voice reminder attached.
            
            Time: {time.strftime('%Y-%m-%d %H:%M:%S')}
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Attach audio file
            with open(audio_file, 'rb') as f:
                audio_attachment = MIMEAudio(f.read())
                audio_attachment.add_header('Content-Disposition', f'attachment; filename={os.path.basename(audio_file)}')
                msg.attach(audio_attachment)
            
            # Gmail SMTP configuration
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.email_address, self.email_password)
            
            # Send email
            text = msg.as_string()
            server.sendmail(self.email_address, self.recipient_email, text)
            server.quit()
            
            return {"status": "success", "message": "Email with audio sent successfully"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def _store_browser_notification(self, message):
        """Store notification for web interface"""
        try:
            # Load existing notifications
            notifications = []
            if os.path.exists(self.notifications_file):
                with open(self.notifications_file, 'r') as f:
                    notifications = json.load(f)
            
            # Add new notification
            notification_data = {
                "id": len(notifications) + 1,
                "message": message,
                "timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
                "read": False
            }
            notifications.append(notification_data)
            
            # Keep only last 50 notifications
            notifications = notifications[-50:]
            
            # Save notifications
            with open(self.notifications_file, 'w') as f:
                json.dump(notifications, f, indent=4)
            
            return {"status": "success", "message": "Browser notification stored"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def get_notifications(self):
        """Get stored notifications for web interface"""
        try:
            if os.path.exists(self.notifications_file):
                with open(self.notifications_file, 'r') as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"Error loading notifications: {e}")
            return []
    
    def mark_notification_read(self, notification_id):
        """Mark a notification as read"""
        try:
            notifications = self.get_notifications()
            for notification in notifications:
                if notification['id'] == notification_id:
                    notification['read'] = True
                    break
            
            with open(self.notifications_file, 'w') as f:
                json.dump(notifications, f, indent=4)
            
            return {"status": "success"}
        except Exception as e:
            return {"status": "error", "message": str(e)}