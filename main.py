from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
import requests
import json
import threading
from datetime import datetime

class ChatMessage(MDCard):
    def __init__(self, text, is_user=True, **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = (0.1, 0.5, 0.8, 1) if is_user else (0.2, 0.2, 0.2, 1)
        self.padding = dp(10)
        self.spacing = dp(5)
        self.size_hint_y = None
        self.height = dp(60)
        self.elevation = 2
        self.radius = [dp(10)]
        
        layout = MDBoxLayout(
            orientation='vertical',
            adaptive_height=True,
            spacing=dp(5)
        )
        
        # Add sender label
        sender_label = MDLabel(
            text='You' if is_user else 'AI Assistant',
            theme_text_color='Primary',
            font_style='Caption',
            size_hint_y=None,
            height=dp(20)
        )
        
        # Add message text
        message_label = MDLabel(
            text=text,
            theme_text_color='Primary',
            text_size=(None, None),
            halign='left',
            valign='top',
            adaptive_height=True
        )
        
        layout.add_widget(sender_label)
        layout.add_widget(message_label)
        self.add_widget(layout)
        
        # Adjust card height based on content
        self.height = max(dp(60), layout.height + dp(20))

class SettingsDialog(MDDialog):
    def __init__(self, app_instance, **kwargs):
        self.app_instance = app_instance
        
        content = MDBoxLayout(
            orientation='vertical',
            spacing=dp(10),
            size_hint_y=None,
            height=dp(200)
        )
        
        self.server_input = MDTextField(
            hint_text='Server URL (e.g., http://192.168.1.100:1234)',
            text=app_instance.server_url,
            size_hint_y=None,
            height=dp(40)
        )
        
        self.model_input = MDTextField(
            hint_text='Model Name',
            text=app_instance.model_name,
            size_hint_y=None,
            height=dp(40)
        )
        
        content.add_widget(MDLabel(text='LM Studio Settings', size_hint_y=None, height=dp(30)))
        content.add_widget(self.server_input)
        content.add_widget(self.model_input)
        
        super().__init__(
            title='Settings',
            content_cls=content,
            buttons=[
                MDRaisedButton(
                    text='Save',
                    on_release=self.save_settings
                ),
                MDRaisedButton(
                    text='Cancel',
                    on_release=self.dismiss
                )
            ],
            **kwargs
        )
    
    def save_settings(self, *args):
        self.app_instance.server_url = self.server_input.text
        self.app_instance.model_name = self.model_input.text
        self.app_instance.save_settings()
        self.dismiss()

class LocalLLMChatApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'Blue'
        
        # Default settings
        self.server_url = 'http://localhost:1234'
        self.model_name = 'local-model'
        self.conversation_history = []
        
        # Load settings
        self.load_settings()
    
    def build(self):
        # Main layout
        main_layout = MDBoxLayout(orientation='vertical')
        
        # Top toolbar
        toolbar = MDTopAppBar(
            title='Local LLM Chat',
            elevation=2,
            right_action_items=[
                ['cog', lambda x: self.open_settings()],
                ['delete', lambda x: self.clear_chat()]
            ]
        )
        
        # Chat area
        self.chat_scroll = MDScrollView()
        self.chat_layout = MDGridLayout(
            cols=1,
            spacing=dp(10),
            padding=dp(10),
            adaptive_height=True,
            size_hint_y=None
        )
        self.chat_scroll.add_widget(self.chat_layout)
        
        # Input area
        input_layout = MDBoxLayout(
            orientation='horizontal',
            adaptive_height=True,
            spacing=dp(10),
            padding=dp(10),
            size_hint_y=None,
            height=dp(60)
        )
        
        self.message_input = MDTextField(
            hint_text='Type your message...',
            multiline=False,
            size_hint_x=0.8
        )
        self.message_input.bind(on_text_validate=self.send_message)
        
        send_button = MDIconButton(
            icon='send',
            theme_icon_color='Primary',
            on_release=self.send_message
        )
        
        input_layout.add_widget(self.message_input)
        input_layout.add_widget(send_button)
        
        # Add all components to main layout
        main_layout.add_widget(toolbar)
        main_layout.add_widget(self.chat_scroll)
        main_layout.add_widget(input_layout)
        
        # Add welcome message
        self.add_message('Hello! I\'m your local AI assistant. How can I help you today?', is_user=False)
        
        return main_layout
    
    def add_message(self, text, is_user=True):
        message = ChatMessage(text, is_user)
        self.chat_layout.add_widget(message)
        
        # Auto-scroll to bottom
        Clock.schedule_once(lambda dt: self.scroll_to_bottom(), 0.1)
    
    def scroll_to_bottom(self):
        self.chat_scroll.scroll_y = 0
    
    def send_message(self, *args):
        message_text = self.message_input.text.strip()
        if not message_text:
            return
        
        # Add user message to chat
        self.add_message(message_text, is_user=True)
        self.message_input.text = ''
        
        # Add to conversation history
        self.conversation_history.append({"role": "user", "content": message_text})
        
        # Send request to LM Studio in background thread
        threading.Thread(target=self.get_ai_response, args=(message_text,)).start()
    
    def get_ai_response(self, user_message):
        try:
            # Prepare the request payload for LM Studio
            payload = {
                "model": self.model_name,
                "messages": self.conversation_history,
                "temperature": 0.7,
                "max_tokens": 1000,
                "stream": False
            }
            
            headers = {
                "Content-Type": "application/json"
            }
            
            # Make request to LM Studio server
            response = requests.post(
                f"{self.server_url}/v1/chat/completions",
                json=payload,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                ai_message = data['choices'][0]['message']['content']
                
                # Add AI response to conversation history
                self.conversation_history.append({"role": "assistant", "content": ai_message})
                
                # Add AI message to chat (on main thread)
                Clock.schedule_once(lambda dt: self.add_message(ai_message, is_user=False))
            else:
                error_msg = f"Error: Server returned status {response.status_code}"
                Clock.schedule_once(lambda dt: self.add_message(error_msg, is_user=False))
        
        except requests.exceptions.ConnectionError:
            error_msg = "Connection Error: Cannot connect to LM Studio server. Please check if LM Studio is running and the server URL is correct."
            Clock.schedule_once(lambda dt: self.add_message(error_msg, is_user=False))
        
        except requests.exceptions.Timeout:
            error_msg = "Timeout Error: The request took too long. Please try again."
            Clock.schedule_once(lambda dt: self.add_message(error_msg, is_user=False))
        
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            Clock.schedule_once(lambda dt: self.add_message(error_msg, is_user=False))
    
    def open_settings(self):
        dialog = SettingsDialog(self)
        dialog.open()
    
    def clear_chat(self):
        self.chat_layout.clear_widgets()
        self.conversation_history = []
        self.add_message('Chat cleared. How can I help you?', is_user=False)
    
    def save_settings(self):
        settings = {
            'server_url': self.server_url,
            'model_name': self.model_name
        }
        try:
            with open('settings.json', 'w') as f:
                json.dump(settings, f)
        except Exception as e:
            print(f"Error saving settings: {e}")
    
    def load_settings(self):
        try:
            with open('settings.json', 'r') as f:
                settings = json.load(f)
                self.server_url = settings.get('server_url', 'http://localhost:1234')
                self.model_name = settings.get('model_name', 'local-model')
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"Error loading settings: {e}")

if __name__ == '__main__':
    LocalLLMChatApp().run()