import tkinter as tk
from tkinter import ttk
import subprocess
import sys

class CutePinkLauncher:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Adventure with Gio")
        self.root.geometry("800x600")
        
        # Define cute pink colors
        self.colors = {
            'bg': '#FFF0F5',          # Light pink background
            'title': '#FF69B4',       # Hot pink for title
            'button': '#FF8FAB',      # Soft pink for buttons
            'button_hover': '#FF6B9E', # Darker pink for hover
            'text': '#FF69B4',        # Hot pink for text
            'subtitle': '#FF69B4'     # Hot pink for subtitle
        }
        
        self.root.configure(bg=self.colors['bg'])
        
        # Create main container
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Title with cute font
        title = tk.Label(
            main_frame,
            text="✨ Adventure with Gio ✨",
            font=('Comic Sans MS', 40, 'bold'),
            fg=self.colors['title'],
            bg=self.colors['bg']
        )
        title.pack(pady=(0, 10))
        
        # Subtitle with hearts
        subtitle = tk.Label(
            main_frame,
            text="♥ Choose Your Magical Journey ♥",
            font=('Comic Sans MS', 20),
            fg=self.colors['subtitle'],
            bg=self.colors['bg']
        )
        subtitle.pack(pady=(0, 50))
        
        # Buttons container
        buttons_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        buttons_frame.pack(pady=20)
        
        # Create cute buttons
        self.create_cute_button(
            buttons_frame,
            "🎀 School Adventure 🎀",
            "Explore the magical school campus with Gio",
            self.launch_school_adventure
        )
        
        self.create_cute_button(
            buttons_frame,
            "🌸 Off-campus Adventure 🌸",
            "Join Gio in an exciting city exploration",
            self.launch_offcampus_adventure
        )
        
        # Cute exit button
        exit_btn = tk.Button(
            main_frame,
            text="✨ Exit ✨",
            font=('Comic Sans MS', 14),
            fg='white',
            bg=self.colors['button'],
            activebackground=self.colors['button_hover'],
            activeforeground='white',
            bd=0,
            width=20,
            height=1,
            cursor='hand2',
            command=self.root.destroy
        )
        exit_btn.pack(pady=(40, 0))
        
        # Add hover effect to exit button
        exit_btn.bind('<Enter>', lambda e: exit_btn.configure(bg=self.colors['button_hover']))
        exit_btn.bind('<Leave>', lambda e: exit_btn.configure(bg=self.colors['button']))

    def create_cute_button(self, parent, title, description, command):
        # Button container
        button_container = tk.Frame(parent, bg=self.colors['bg'])
        button_container.pack(pady=15)
        
        # Main button
        button = tk.Button(
            button_container,
            text=title,
            font=('Comic Sans MS', 18),
            fg='white',
            bg=self.colors['button'],
            activebackground=self.colors['button_hover'],
            activeforeground='white',
            bd=0,
            width=25,
            height=1,
            cursor='hand2',
            command=command
        )
        button.pack()
        
        # Description with cute font
        description_label = tk.Label(
            button_container,
            text=description,
            font=('Comic Sans MS', 12),
            fg=self.colors['text'],
            bg=self.colors['bg']
        )
        description_label.pack(pady=(5, 0))
        
        # Hover effects
        def on_enter(e):
            button['background'] = self.colors['button_hover']
            
        def on_leave(e):
            button['background'] = self.colors['button']
            
        button.bind('<Enter>', on_enter)
        button.bind('<Leave>', on_leave)

    def launch_school_adventure(self):
        self.root.iconify()
        try:
            subprocess.run([sys.executable, "school_adventure.py"])
        finally:
            self.root.deiconify()

    def launch_offcampus_adventure(self):
        self.root.iconify()
        try:
            subprocess.run([sys.executable, "Off-campus adventure.py"])
        finally:
            self.root.deiconify()

    def run(self):
        # Center window on screen
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        # Make window non-resizable
        self.root.resizable(False, False)
        
        self.root.mainloop()

if __name__ == "__main__":
    launcher = CutePinkLauncher()
    launcher.run()