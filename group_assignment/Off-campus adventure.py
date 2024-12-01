import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
import json
import os
from PIL import Image, ImageTk
from pathlib import Path

image_folder = Path(__file__).parent / "images"
images = {}

for image in image_folder.iterdir():
    images[image.stem] = Image.open(image)





class GioGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Adventure with Gio")
        self.root.geometry("1024x768")
        self.root.configure(background='white')
        
        # Game data initialization
        self.days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        self.current_day = 0
        self.affection = 0
        self.gio_mood = ""
        self.energy = 100
        self.money = 1000
        self.inventory = ['Seafood Rice', 'Italian Coffee', 'Rose', 'Tiramisu']
        self.visited_places = set()
        self.daily_visits = 0
        self.achievements = set()
        
        # Game content
        self.load_game_content()
        self.setup_gui()
        self.load_save_game()
        
    def load_game_content(self):
        # Locations and basic actions
        self.locations = {
            'Classroom': ['Attend Class', 'Ask Questions', 'Help Organize', 'Give Gift', 'Chat'],
            'Beach': ['Take a Walk', 'Take Photos', 'Collect Shells', 'Give Gift', 'Have Lunch'],
            'Cinema': ['Watch Movie', 'Buy Popcorn', 'Discuss Plot', 'Give Gift', 'Plan Next Time'],
            'Library': ['Study Together', 'Find Materials', 'Discuss Paper', 'Give Gift', 'Help Organize Books'],
            'Study Room': ['Review', 'Discuss Problems', 'Help Others', 'Give Gift', 'Share Notes'],
            'Mall': ['Shopping', 'Drink Coffee', 'Visit Bookstore', 'Give Gift', 'Have Dinner'],
            'Dessert Shop': ['Taste Desserts', 'Chat', 'Take Photos', 'Give Gift', 'Recommend Food'],
            'Forest Park': ['Walk', 'Observe Plants', 'Feed Animals', 'Give Gift', 'Picnic'],
            'Computer Lab': ['Debug Programs', 'Fix Bugs', 'Help Classmates', 'Give Gift', 'Discuss Projects'],
            'Cafe': ['Drink Coffee', 'Chat', 'Read Books', 'Give Gift', 'Share Stories']
        }
        
        # Dialogue database
        self.dialogue_database = {
            'Classroom': {
                'Attend Class': [
                    ("Today's lecture is fascinating!", "I agree, especially the theoretical part."),
                    ("Did you understand that last concept?", "Maybe we can discuss it during break?"),
                    ("*Taking detailed notes*", "*Trying to keep up with the pace*")
                ],
                'Ask Questions': [
                    ("That's an excellent question!", "Thanks for the detailed explanation."),
                    ("Let me think about this...", "Take your time, I'm curious too."),
                    ("You always ask great questions!", "I try to understand things thoroughly")
                ]
            },
            'Cafe': {
                'Drink Coffee': [
                    ("This reminds me of Italian coffee...", "Tell me more about your experiences!"),
                    ("Try this special blend!", "Thanks, it smells amazing!"),
                    ("Perfect weather for coffee", "And perfect company too!")
                ],
                'Chat': [
                    ("How's your research going?", "Making progress, slowly but surely."),
                    ("Any interesting papers lately?", "Yes, let me share them with you!"),
                    ("*Enjoying peaceful atmosphere*", "*Feeling content*")
                ]
            }
        }
        
        # Special events
        self.special_events = {
            'Library': {
                'title': 'Late Night Study',
                'description': "It's getting late at the library...",
                'options': [
                    ("Suggest taking a break", 15),
                    ("Keep studying together", 20),
                    ("Bring Gio some coffee", 25),
                    ("Fall asleep on books", -10)
                ]
            },
            'Mall': {
                'title': 'Shopping Adventure',
                'description': "Gio seems interested in a research book...",
                'options': [
                    ("Buy it as a surprise", 30),
                    ("Discuss the topic", 20),
                    ("Suggest another book", 10),
                    ("Ignore and walk away", -15)
                ]
            }
        }
        
        # Items and their effects
        self.items = {
            'Seafood Rice': {'affection': 15, 'energy': 20},
            'Italian Coffee': {'affection': 20, 'energy': 30},
            'Rose': {'affection': 25, 'energy': 0},
            'Tiramisu': {'affection': 20, 'energy': 15},
            'Research Paper': {'affection': 15, 'energy': -10},
            'Laptop': {'affection': 10, 'energy': -5},
            'Study Notes': {'affection': 10, 'energy': -5},
            'Camera': {'affection': 15, 'energy': 0},
            'Novel': {'affection': 10, 'energy': 5},
            'Chocolate': {'affection': 15, 'energy': 10}
        }
        
        # Achievements
        self.achievement_conditions = {
            'First Step': 'Visit first location',
            'Coffee Lover': 'Drink coffee 5 times',
            'Bookworm': 'Study in library 10 times',
            'True Friend': 'Reach 50 affection',
            'Perfect Match': 'Reach 100 affection'
        }

    def setup_gui(self):
        # Main container
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Status area
        self.setup_status_area()
        
        # Main game area
        self.setup_game_area()
        
        # Inventory and dialog area
        self.setup_inventory_dialog()
        
        # Control buttons
        self.setup_controls()
        
        # Initial GUI update
        self.update_gui()

    def setup_status_area(self):
        status_frame = ttk.LabelFrame(self.main_frame, text="Status", padding="5")
        status_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E))
        
        self.status_labels = {}
        status_items = [
            ('day', "Day"), 
            ('affection', "Affection"),
            ('energy', "Energy"),
            ('money', "Money"),
            ('mood', "Gio's Mood")
        ]
        
        for i, (key, text) in enumerate(status_items):
            self.status_labels[key] = ttk.Label(status_frame, text=f"{text}: 0")
            self.status_labels[key].grid(row=0, column=i, padx=5)

    def setup_game_area(self):
        # Location selection
        location_frame = ttk.LabelFrame(self.main_frame, text="Locations", padding="5")
        location_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.location_listbox = tk.Listbox(location_frame, height=10)
        self.location_listbox.pack(fill=tk.BOTH, expand=True)
        
        # Action selection
        action_frame = ttk.LabelFrame(self.main_frame, text="Actions", padding="5")
        action_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.action_listbox = tk.Listbox(action_frame, height=10)
        self.action_listbox.pack(fill=tk.BOTH, expand=True)
        
        # Character display
        self.setup_character_display()

    def setup_character_display(self):
        character_frame = ttk.LabelFrame(self.main_frame, text="Gio", padding="5")
        character_frame.grid(row=1, column=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Character canvas (for avatar)
        self.character_canvas = tk.Canvas(character_frame, width=200, height=200)
        self.character_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Draw simple avatar (placeholder)
        self.draw_avatar()

    def setup_inventory_dialog(self):
        # Inventory
        inventory_frame = ttk.LabelFrame(self.main_frame, text="Inventory", padding="5")
        inventory_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E))
        self.current_item = False
        
        def select_item(evt):
            selection = self.inventory_listbox.curselection()
            if selection:
                self.current_item = selection
        
        self.inventory_listbox = tk.Listbox(inventory_frame, height=4)
        self.inventory_listbox.pack(fill=tk.BOTH, expand=True)
        self.inventory_listbox.bind('<<ListboxSelect>>', select_item)
        
        # Dialog box
        dialog_frame = ttk.LabelFrame(self.main_frame, text="Dialog", padding="5")
        dialog_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E))
        
        self.dialog_text = tk.Text(dialog_frame, height=6, wrap=tk.WORD)
        self.dialog_text.pack(fill=tk.BOTH, expand=True)

    def setup_controls(self):
        control_frame = ttk.Frame(self.main_frame, padding="5")
        control_frame.grid(row=4, column=0, columnspan=3)
        
        buttons = [
            ("Visit", self.visit_location),
            ("End Day", self.end_day),
            ("Save", self.save_game),
            ("Load", self.load_save_game),
            ("Help", self.show_help)
        ]
        
        for i, (text, command) in enumerate(buttons):
            ttk.Button(control_frame, text=text, command=command).grid(row=0, column=i, padx=5)

    def draw_avatar(self):
        
        
        img = images[f'gio_{self.gio_mood}']
        self.character_canvas.image = ImageTk.PhotoImage(img.resize((200, 200), Image.Resampling.BILINEAR))
        self.character_canvas.create_image(0, 0, image=self.character_canvas.image, anchor='nw')
        
        # Simple placeholder avatar
        # self.character_canvas.delete("all")
        # self.character_canvas.create_oval(50, 50, 150, 150, fill="beige")
        
        # # Expression changes based on mood
        # if self.gio_mood:
        #     # Happy expression
        #     self.character_canvas.create_arc(75, 75, 125, 125, start=0, extent=-180, fill="black")
        # else:
        #     # Sad expression
        #     self.character_canvas.create_arc(75, 100, 125, 150, start=0, extent=180, fill="black")

    def update_gui(self):
        print(self.inventory_listbox.curselection())
        # Update status labels
        self.status_labels['day'].config(text=f"Day: {self.days[self.current_day]}")
        self.status_labels['affection'].config(text=f"Affection: {self.affection}")
        self.status_labels['energy'].config(text=f"Energy: {self.energy}")
        self.status_labels['money'].config(text=f"Money: ${self.money}")
        self.status_labels['mood'].config(text=f"Mood: {'Good' if self.gio_mood else 'Bad'}")
        
        # Update location list
        self.location_listbox.delete(0, tk.END)
        for loc in self.locations:
            if loc not in self.visited_places:
                self.location_listbox.insert(tk.END, loc)
        
        # Update inventory
        self.inventory_listbox.delete(0, tk.END)
        for item in self.inventory:
            self.inventory_listbox.insert(tk.END, item)
        
        # Update avatar
        self.draw_avatar()

    def visit_location(self):
        if self.energy < 10:
            messagebox.showinfo("Notice", "Too tired! End the day to rest.")
            return
            
        if self.daily_visits >= 2:
            messagebox.showinfo("Notice", "You've visited two locations today.")
            return
            
        selection = self.location_listbox.curselection()
        if not selection:
            messagebox.showinfo("Notice", "Please select a location")
            return
            
        location = self.location_listbox.get(selection[0])
        
        # Update action list
        self.action_listbox.delete(0, tk.END)
        for action in self.locations[location]:
            self.action_listbox.insert(tk.END, action)
        
        # Bind double-click event
        self.action_listbox.bind('<Double-Button-1>', 
                               lambda e: self.perform_action(location))
        
        # Random special event
        if random.random() < 0.3:
            self.trigger_special_event(location)
        
        self.daily_visits += 1
        self.visited_places.add(location)
        self.energy -= 10
        self.update_gui()

    def perform_action(self, location):
        selection = self.action_listbox.curselection()
        if not selection:
            messagebox.showinfo("Notice", "Please select an action")
            return
            
        action = self.action_listbox.get(selection[0])
        
        # Handle action
        if action == 'Give Gift':
            self.give_gift()
        else:
            self.handle_normal_action(location, action)
        
        # Random item acquisition
        if random.random() < 0.3:
            self.acquire_random_item()
        
        self.update_gui()

    def handle_normal_action(self, location, action):
        is_good = random.random() > 0.4
        self.generate_event(location, action, is_good)
        
        # Calculate changes
        change = random.randint(5, 15) if is_good else random.randint(-15, -5)
        if self.gio_mood:
            change = int(change * 1.5)
            
        self.affection += change
        self.energy -= 5

        outcome = random.random() > 0.3
        
        self.gio_mood = "happy" if outcome else "sad"
        self.draw_avatar()

    def give_gift(self):
        if not self.inventory:
            messagebox.showinfo("Notice", "No gifts available!")
            return
            
        selection = self.current_item
        if not selection:
            messagebox.showinfo("Notice", "Please select a gift")
            return
            
        gift = self.inventory_listbox.get(selection[0])
        self.inventory.remove(gift)
        
        # Apply gift effects
        if gift in self.items:
            effects = self.items[gift]
            self.affection += effects['affection']
            self.energy += effects['energy']
            
            self.dialog_text.insert(tk.END, 
                f"\nGave {gift}\nAffection +{effects['affection']}\nEnergy {effects['energy']:+}\n")
        
        self.update_gui()

    def acquire_random_item(self):
        new_item = random.choice(list(self.items.keys()))
        self.inventory.append(new_item)
        self.dialog_text.insert(tk.END, f"\nObtained: {new_item}\n")

    def trigger_special_event(self, location):
        if location in self.special_events:
            event = self.special_events[location]
            options = [f"{i+1}. {opt[0]}" for i, opt in enumerate(event['options'])]
            
            response = messagebox.askquestion(
                event['title'],
                event['description'] + "\n\n" + "\n".join(options)
            )
            
            if response == 'yes':
                selected = 0  # Default to first option
                change = event['options'][selected][1]
                self.affection += change
                self.dialog_text.insert(tk.END, 
                    f"\nSpecial event result: Affection change {change}\n")

    def generate_event(self, location, action, is_good):
        self.dialog_text.delete(1.0, tk.END)
        
        if location in self.dialogue_database and action in self.dialogue_database[location]:
            dialogue = random.choice(self.dialogue_database[location][action])
        else:
            if is_good:
                dialogue = random.choice([
                    ("What a wonderful day!", "Indeed it is!"),
                    ("You're amazing!", "Thanks, you too!"),
                    ("This is fun!", "Let's do it again sometime!")
                ])
            else:
                dialogue = random.choice([
                    ("*Looks tired*", "Should we take a break?"),
                    ("Maybe next time...", "I'll try better!"),
                    ("*Checks phone*", "Everything okay?")
                ])
        
        self.show_dialogue_with_animation(dialogue)

    def show_dialogue_with_animation(self, dialogue_pair):
        self.dialog_text.delete(1.0, tk.END)
        
        for line in dialogue_pair:
            for char in line:
                self.dialog_text.insert(tk.END, char)
                self.dialog_text.see(tk.END)
                self.root.update()
                time.sleep(0.03)
            self.dialog_text.insert(tk.END, "\n")
            time.sleep(0.5)

    def end_day(self):
        self.current_day = (self.current_day + 1) % 7
        self.daily_visits = 0
        self.visited_places.clear()
        self.energy = 100
        
        if self.current_day == 0:  # Week completed
            self.show_ending()
        else:
            self.update_gui()

    def show_ending(self):
        ending_text = "Game Over!\n\n"
        ending_text += f"Final Affection: {self.affection}\n\n"
        
        if self.affection <= 20:
            ending_text += "Ending: Academic Strangers\n"
            ending_text += "Sometimes paths just don't align..."
        elif self.affection <= 50:
            ending_text += "Ending: Casual Friends\n"
            ending_text += "You maintained a pleasant academic relationship."
        elif self.affection <= 80:
            ending_text += "Ending: Close Friends\n"
            ending_text += "You developed a strong friendship!"
        elif self.affection <= 100:
            ending_text += "Ending: Best Friends\n"
            ending_text += "Your friendship will last a lifetime!"
        else:
            ending_text += "Ending: Perfect Partnership\n"
            ending_text += "You achieved both academic success and perfect friendship!"
        
        messagebox.showinfo("Game Over", ending_text)
        if messagebox.askyesno("New Game", "Would you like to start a new game?"):
            self.__init__(self.root)
        else:
            self.root.quit()

    def save_game(self):
        save_data = {
            'day': self.current_day,
            'affection': self.affection,
            'energy': self.energy,
            'money': self.money,
            'mood': self.gio_mood,
            'inventory': self.inventory,
            'achievements': list(self.achievements)
        }
        
        with open('save_game.json', 'w') as f:
            json.dump(save_data, f)
        
        messagebox.showinfo("Save", "Game saved successfully!")

    def load_save_game(self):
        try:
            with open('save_game.json', 'r') as f:
                save_data = json.load(f)
                
            self.current_day = save_data['day']
            self.affection = save_data['affection']
            self.energy = save_data['energy']
            self.money = save_data['money']
            self.gio_mood = save_data['mood']
            self.inventory = save_data['inventory']
            self.achievements = set(save_data['achievements'])
            
            self.update_gui()
            messagebox.showinfo("Load", "Game loaded successfully!")
        except:
            messagebox.showerror("Error", "No save file found or error loading save.")

    def show_help(self):
        help_text = """
Game Instructions:

1. Visit locations and perform actions to increase affection
2. Manage your energy levels
3. Give gifts to boost relationship
4. Special events may occur randomly
5. Save your progress regularly
6. Try to achieve different endings

Controls:
- Double click actions to perform them
- Use buttons for main controls
- Check status bar for current state

Tips:
- Different gifts have different effects
- Mood affects affection gains
- Rest when energy is low
- Try to experience all locations
"""
        messagebox.showinfo("Help", help_text)

if __name__ == "__main__":
    try:
        root = tk.Tk()
        game = GioGame(root)
        root.mainloop()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()