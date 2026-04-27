import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox
from datetime import datetime

class ChatClient:
    #A multi-language chat client application with dark/light mode support.
    #Allows real-time messaging, private messages, and language switching.
    
    
    def __init__(self, master):
        # Main window setup
        self.master = master
        self.master.title("Chat Application")
        self.master.geometry("500x600")
        self.master.resizable(False, False)
        self.master.configure(bg="#2E3440")

        # Initialize state variables
        self.is_dark_mode = True
        self.language = 'en'
        self.translations = self.get_translations()
        self.running = True
        self.last_sent_message = None

        # Network configuration
        self.server_host = "localhost"
        self.server_port = 25000
        self.client_socket = None

        self._setup_ui()
        self._configure_chat_tags()
        self.connect_to_server()

    def _setup_ui(self):
        #Setup all UI components of the chat application
        # Header section
        self.header_frame = tk.Frame(self.master, bg="#3B4252")
        self.header_frame.pack(fill=tk.X, pady=(10, 5))

        self.header = tk.Label(
            self.header_frame,
            text=self.translations[self.language]['chat_header'],
            bg="#3B4252",
            fg="white",
            font=("Arial", 16, "bold")
        )
        self.header.pack(side=tk.LEFT, padx=10)

        # Control buttons
        self.toggle_button = tk.Button(
            self.header_frame,
            text=self.translations[self.language]['toggle_button_text'],
            command=self.toggle_mode,
            bg="#D08770",
            fg="black",
            font=("Arial", 12),
            relief="flat"
        )
        self.toggle_button.pack(side=tk.RIGHT, padx=10)

        self.settings_button = tk.Button(
            self.header_frame,
            text=self.translations[self.language]['settings_button'],
            command=self.open_settings,
            bg="#D08770",
            fg="black",
            font=("Arial", 12),
            relief="flat"
        )
        self.settings_button.pack(side=tk.RIGHT, padx=10)

        # Chat area
        self.chat_area = scrolledtext.ScrolledText(
            self.master,
            wrap=tk.WORD,
            state="disabled",
            bg="#4C566A",
            fg="white",
            font=("Arial", 12)
        )
        self.chat_area.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        # Message input section
        self._setup_message_input()

    def _setup_message_input(self):
        #Setup message input area and related buttons
        self.entry_frame = tk.Frame(self.master, bg="#2E3440")
        self.entry_frame.pack(fill=tk.X, pady=10)

        self.message_entry = tk.Entry(
            self.entry_frame,
            font=("Arial", 12),
            bg="#3B4252",
            fg="white",
            insertbackground="white"
        )
        self.message_entry.pack(side=tk.LEFT, padx=10, pady=5, fill=tk.X, expand=True)
        self.message_entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(
            self.entry_frame,
            text=self.translations[self.language]['send_button'],
            command=self.send_message,
            bg="#88C0D0",
            fg="black",
            font=("Arial", 12)
        )
        self.send_button.pack(side=tk.RIGHT, padx=10, pady=5)

        self.disconnect_button = tk.Button(
            self.master,
            text=self.translations[self.language]['disconnect_button'],
            command=self.disconnect,
            bg="#BF616A",
            fg="white",
            font=("Arial", 12)
        )
        self.disconnect_button.pack(padx=10, pady=10, fill=tk.X)

    def _configure_chat_tags(self):
        #Configure text tags for different message types in chat
        self.chat_area.tag_config("user", foreground="#A3BE8C")
        self.chat_area.tag_config("received", foreground="#88C0D0")
        self.chat_area.tag_config("system", foreground="#D08770")
        self.chat_area.tag_config("mention", foreground="red", font=("Arial", 12, "bold"))

    def get_translations(self):
        #Return dictionary of translations for all supported languages
        return {
            'en': {
                'chat_header': "Chat Application",
                'toggle_button_text': "Switch to Light Mode",
                'send_button': "Send",
                'disconnect_button': "Disconnect",
                'system_message': "System Message",
                'connected_message': "Connected to the server!",
                'disconnect_message': "Disconnected from the server!",
                'settings_button': "Settings"
            },
            'es': {
                'chat_header': "Aplicación de Chat",
                'toggle_button_text': "Cambiar a Modo Claro",
                'send_button': "Enviar",
                'disconnect_button': "Desconectar",
                'system_message': "Mensaje del Sistema",
                'connected_message': "¡Conectado al servidor!",
                'disconnect_message': "¡Desconectado del servidor!",
                'settings_button': "Configuración"
            },
            'fr': {
                'chat_header': "Application de Chat",
                'toggle_button_text': "Passer au Mode Clair",
                'send_button': "Envoyer",
                'disconnect_button': "Se Déconnecter",
                'system_message': "Message du Système",
                'connected_message': "Connecté au serveur!",
                'disconnect_message': "Déconnecté du serveur!",
                'settings_button': "Paramètres"
            },
            'de': {
                'chat_header': "Chat-Anwendung",
                'toggle_button_text': "Wechseln zum Hellen Modus",
                'send_button': "Senden",
                'disconnect_button': "Trennen",
                'system_message': "Systemnachricht",
                'connected_message': "Mit dem Server verbunden!",
                'disconnect_message': "Vom Server getrennt!",
                'settings_button': "Einstellungen"
            },
            'zh': {
                'chat_header': "聊天应用",
                'toggle_button_text': "切换到亮模式",
                'send_button': "发送",
                'disconnect_button': "断开连接",
                'system_message': "系统消息",
                'connected_message': "已连接到服务器！",
                'disconnect_message': "已断开与服务器的连接！",
                'settings_button': "设置"
            }
        }

    def connect_to_server(self):
        #Establish connection to chat server
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.server_host, self.server_port))
            self.add_message(self.translations[self.language]['connected_message'], system_message=True)
            threading.Thread(target=self.receive_messages, daemon=True).start()
        except Exception as e:
            messagebox.showerror("Connection Error", f"Could not connect to the server: {e}")
            self.master.destroy()

    def receive_messages(self):
        #Handle incoming messages from server
        while self.running:
            try:
                message = self.client_socket.recv(2048).decode()
                if message and message != self.last_sent_message:
                    self.add_message(message, user_message=False)
                else:
                    break
            except Exception as e:
                self.add_message(f"Error receiving message: {e}", system_message=True)
                break
        self.running = False
        self.client_socket.close()

    def send_message(self, event=None):
        #Handle sending messages to server
        message = self.message_entry.get().strip()
        if not message:
            return

        if message.startswith("/pm"):
            self._handle_private_message(message)
        else:
            self._handle_regular_message(message)

    def _handle_private_message(self, message):
        #Process and send private messages
        parts = message.split(" ", 2)
        if len(parts) >= 3:
            recipient, pm_message = parts[1], parts[2]
            try:
                self.client_socket.send(f"/pm {recipient} {pm_message}".encode())
                self._post_message_actions()
            except Exception as e:
                self.add_message(f"Error sending private message: {e}", system_message=True)
        else:
            self.add_message("Invalid private message format. Use '/pm <username> <message>'", system_message=True)

    def _handle_regular_message(self, message):
        #Process and send regular messages
        try:
            self.client_socket.send(message.encode())
            self.last_sent_message = message
            self.add_message(f"You: {message}", user_message=True)
            self._post_message_actions()
        except Exception as e:
            self.add_message(f"Error sending message: {e}", system_message=True)

    def _post_message_actions(self):
        #Actions to perform after sending any message
        self.message_entry.delete(0, tk.END)
        self.send_button.config(state=tk.DISABLED)
        self.master.after(1000, self.enable_send_button)

    def enable_send_button(self):
        #Re-enable the send button
        self.send_button.config(state=tk.NORMAL)

    def add_message(self, message, user_message=False, system_message=False):
        #Add a message to the chat area with appropriate formatting
        self.chat_area.config(state="normal")
        
        # Add timestamp
        timestamp = f"[{self.get_timestamp()}] "
        self.chat_area.tag_config("timestamp", foreground="#D8DEE9")
        self.chat_area.insert(tk.END, timestamp, "timestamp")

        # Add system message prefix if needed
        if system_message:
            self.chat_area.insert(tk.END, f"[{self.translations[self.language]['system_message']}]: ", "system")

        # Process and insert message words
        words = str(message).split()
        for i, word in enumerate(words):
            if word.startswith('@'):
                self.chat_area.insert(tk.END, word, "mention")
            else:
                tag = "user" if user_message else "received" if not system_message else "system"
                self.chat_area.insert(tk.END, word, tag)
            
            if i < len(words) - 1:
                self.chat_area.insert(tk.END, " ")

        self.chat_area.insert(tk.END, "\n")
        self.chat_area.yview(tk.END)
        self.chat_area.config(state="disabled")

    def disconnect(self):
        #Handle client disconnection
        self.running = False
        self.client_socket.close()
        self.add_message(self.translations[self.language]['disconnect_message'], system_message=True)
        self.master.destroy()

    def toggle_mode(self):
        #Toggle between light and dark mode
        if self.is_dark_mode:
            # Switch to light mode
            self.master.configure(bg="#2E3440")
            self.chat_area.config(bg="#E8E8E8", fg="#000000")
            self.message_entry.config(bg="#FFFFFF", fg="#000000")
            self.toggle_button.config(text="Switch to Dark Mode", bg="#FF9800")
            self.chat_area.tag_config("user", foreground="#2E3440")
            self.chat_area.tag_config("received", foreground="#4C566A")
            self.chat_area.tag_config("timestamp", foreground="black")
        else:
            # Switch to dark mode
            self.master.configure(bg="#2E3440")
            self.chat_area.config(bg="#4C566A", fg="white")
            self.message_entry.config(bg="#3B4252", fg="white")
            self.toggle_button.config(text="Switch to Light Mode", bg="#D08770")
            self.chat_area.tag_config("user", foreground="#A3BE8C")
            self.chat_area.tag_config("received", foreground="#88C0D0")
            self.chat_area.tag_config("timestamp", foreground="#D8DEE9")
        self.is_dark_mode = not self.is_dark_mode

    def open_settings(self):
        #Open the settings window for language selection
        settings_window = tk.Toplevel(self.master)
        settings_window.title(self.translations[self.language]['settings_button'])
        settings_window.geometry("200x250")
        
        tk.Label(settings_window, text="Select Language", font=("Arial", 12)).pack(pady=10)

        language_buttons = [
            ("en", "English"),
            ("es", "Español"),
            ("fr", "Français"),
            ("de", "Deutsch"),
            ("zh", "中文")
        ]
        
        for lang_code, lang_name in language_buttons:
            tk.Button(
                settings_window,
                text=lang_name,
                command=lambda lc=lang_code: self.set_language(lc, settings_window)
            ).pack(pady=5)

    def set_language(self, language_code, settings_window):
        #Change the application language
        self.language = language_code
        self.update_texts()
        settings_window.destroy()

    def update_texts(self):
        #Update all UI texts after language change
        self.header.config(text=self.translations[self.language]['chat_header'])
        self.toggle_button.config(text=self.translations[self.language]['toggle_button_text'])
        self.send_button.config(text=self.translations[self.language]['send_button'])
        self.disconnect_button.config(text=self.translations[self.language]['disconnect_button'])
        self.settings_button.config(text=self.translations[self.language]['settings_button'])

    def get_timestamp(self):
        #Return current timestamp in specified format
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

if __name__ == "__main__":
    root = tk.Tk()
    client = ChatClient(root)
    root.option_add("*Font", "Arial 12")
    root.mainloop()