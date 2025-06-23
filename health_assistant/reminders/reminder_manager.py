import schedule
import datetime
import os
import sys
from gtts import gTTS

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from messaging.message_sender import MessageSender

class ReminderManager:
    def __init__(self):
        self.reminders = {}  # Dictionary to store reminders with medication ID as key
        self.message_sender = MessageSender()
        
    def add_reminder(self, medication):
        """Add a new medication reminder"""
        med_id = medication['id']
        name = medication['name']
        time_str = medication['time']
        frequency = medication['frequency']
        
        # Remove existing reminder if it exists
        self.remove_reminder(med_id)
        
        # Schedule based on frequency
        if frequency == 'daily':
            job = schedule.every().day.at(time_str).do(
                self.send_reminder, med_id, name, medication.get('dosage', ''), medication.get('instructions', '')
            )
            self.reminders[med_id] = job
        elif frequency == 'weekly':
            days = medication.get('days', [])
            for day in days:
                if day.lower() == 'monday':
                    job = schedule.every().monday.at(time_str).do(
                        self.send_reminder, med_id, name, medication.get('dosage', ''), medication.get('instructions', '')
                    )
                elif day.lower() == 'tuesday':
                    job = schedule.every().tuesday.at(time_str).do(
                        self.send_reminder, med_id, name, medication.get('dosage', ''), medication.get('instructions', '')
                    )
                # Add other days similarly
                self.reminders[med_id] = job
        elif frequency.startswith('every'):
            try:
                hours = int(frequency.split()[1])
                job = schedule.every(hours).hours.do(
                    self.send_reminder, med_id, name, medication.get('dosage', ''), medication.get('instructions', '')
                )
                self.reminders[med_id] = job
            except (ValueError, IndexError):
                print(f"Invalid frequency format: {frequency}")
    
    def remove_reminder(self, med_id):
        """Remove a medication reminder"""
        if med_id in self.reminders:
            schedule.cancel_job(self.reminders[med_id])
            del self.reminders[med_id]
    
    def send_reminder(self, med_id, name, dosage, instructions):
        """Send a reminder for medication"""
        # Create reminder message
        message = f"Reminder: Time to take {name}"
        if dosage:
            message += f", {dosage}"
        if instructions:
            message += f". {instructions}"
        
        # Create voice note
        self._create_voice_note(message, med_id)
        
        # Send text message
        self.message_sender.send_text_message(message)
        
        # Send voice note
        voice_path = f"temp/voice_{med_id}.mp3"
        if os.path.exists(voice_path):
            self.message_sender.send_voice_message(voice_path, message)
    
    def _create_voice_note(self, message, med_id):
        """Create a voice note from text"""
        os.makedirs('temp', exist_ok=True)
        voice_path = f"temp/voice_{med_id}.mp3"
        
        try:
            tts = gTTS(text=message, lang='en')
            tts.save(voice_path)
            return voice_path
        except Exception as e:
            print(f"Error creating voice note: {e}")
            return None