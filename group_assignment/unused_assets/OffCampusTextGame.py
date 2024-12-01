import random
import time
from typing import List, Dict, Tuple

class Game:
    def __init__(self):
        self.days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        self.current_day = 0
        self.affection = 0
        self.gio_mood = True  # True for good mood, False for bad mood
        
        self.locations = {
            'Classroom': False,
            'Beach': False,
            'Cinema': False,
            'Library': False,
            'Study Room': False,
            'Mall': False,
            'Dessert Shop': False,
            'Forest Park': False,
            'Computer Lab': False,
            'Cafe': False
        }
        
        self.inventory = ['Seafood Rice', 'Italian Coffee', 'Rose', 'Tiramisu']
        
        self.possible_items = [
            'Breath Spray', 'Attendance Code', 'Mouse', 'Microphone', 'Ham Slice',
            'Gun', 'Diamond Ring', 'Antique Wine Glass', 'Truant Student',
            'Failed Student', 'Teaching Assistant'
        ]
        
        self.actions = {
            'Classroom': ['Take notes', 'Chat with Gio', 'Ask questions', 'Share snacks', 'Give a gift'],
            'Beach': ['Build sandcastle', 'Watch sunset', 'Collect shells', 'Go swimming', 'Give a gift'],
            'Cinema': ['Watch movie', 'Share popcorn', 'Hold hands', 'Discuss plot', 'Give a gift'],
            # ... similar actions for other locations
        }

    def get_random_dialogue(self, event_type: str) -> List[str]:
        good_dialogues = {
            'Classroom': [
                "Gio: Today's lecture is interesting!",
                "You: I agree, the examples are helpful.",
                "Gio: Let's study together later!",
                "You: That would be great!",
                "Gio: You're a good study partner!"
            ],
            # ... similar dialogues for other locations
        }
        
        bad_dialogues = {
            'Classroom': [
                "Gio: I'm so tired today...",
                "You: The lecture is boring, right?",
                "Gio: We should focus more.",
                "You: Sorry, you're right.",
                "Gio: Let's try to pay attention."
            ],
            # ... similar dialogues for other locations
        }
        
        return good_dialogues[event_type] if random.random() > 0.5 else bad_dialogues[event_type]

    def special_classroom_event(self):
        print("\nSPECIAL EVENT: Students are fighting in class!")
        choices = [
            "Join the fight",
            "Use this chance to skip class",
            "Push Gio into the crowd",
            "Call security",
            "Record and post online"
        ]
        
        for i, choice in enumerate(choices, 1):
            print(f"{i}. {choice}")
        
        choice = int(input("What will you do? ")) - 1
        results = [
            (-30, "Gio is disappointed in your behavior."),
            (-20, "Gio notices your absence."),
            (-50, "Gio is hurt and angry!"),
            (30, "Gio admires your responsible action."),
            (-10, "Gio thinks that was inappropriate.")
        ]
        
        self.affection += results[choice][0]
        print(results[choice][1])

    def handle_location(self, location: str):
        print(f"\nYou are at the {location}")
        if location == 'Classroom' and random.random() < 0.2:
            self.special_classroom_event()
            return

        actions = self.actions[location]
        for i, action in enumerate(actions, 1):
            print(f"{i}. {action}")
        
        choice = int(input("Choose your action: ")) - 1
        if actions[choice] == 'Give a gift' and self.inventory:
            self.give_gift()
        else:
            self.handle_random_event(location)

        # Random item drop
        if random.random() < 0.3:
            item = random.choice(self.possible_items)
            self.inventory.append(item)
            print(f"\nYou found: {item}")

    def give_gift(self):
        print("\nYour inventory:")
        for i, item in enumerate(self.inventory, 1):
            print(f"{i}. {item}")
        
        choice = int(input("Choose a gift: ")) - 1
        gift = self.inventory.pop(choice)
        
        base_points = random.randint(5, 15)
        bonus = 1.5 if self.gio_mood else 1.0
        gift_points = int(base_points * bonus)
        
        self.affection += gift_points
        print(f"\nGio loved the {gift}! Affection +{gift_points}")

    def handle_random_event(self, location: str):
        is_good = random.random() > 0.5
        self.gio_mood = is_good
        
        dialogues = self.get_random_dialogue(location)
        for dialogue in dialogues:
            print(dialogue)
            time.sleep(1)
        
        base_points = random.randint(5, 15)
        modifier = 1.5 if self.gio_mood else 0.5
        points = int(base_points * modifier)
        
        if is_good:
            self.affection += points
            print(f"\nGood event! Affection +{points}")
        else:
            self.affection -= points
            print(f"\nBad event! Affection -{points}")

    def get_ending(self) -> str:
        if self.affection <= 20:
            return "Ending 1: Delayed graduation..."
        elif self.affection <= 50:
            return "Ending 2: Gio forgets you, but you graduate."
        elif self.affection <= 70:
            return "Ending 3: Good friends with Gio, graduated with distinction!"
        elif self.affection <= 99:
            return "Ending 4: Best friends with Gio, became Gio's PhD student!"
        else:
            return "Ending 5: Academic success with Gio and opened a pineapple pizza shop! *Gio gives you a pizza and a kiss*"

    def play(self):
        print("Welcome to Adventure with Gio!")
        
        while self.current_day < len(self.days):
            print(f"\nDay {self.current_day + 1}: {self.days[self.current_day]}")
            print(f"Current Affection: {self.affection}")
            print("\nAvailable locations:")
            
            available = [loc for loc, visited in self.locations.items() if not visited]
            for i, loc in enumerate(available, 1):
                print(f"{i}. {loc}")
            
            for _ in range(2):
                if not available:
                    break
                choice = int(input("\nChoose location (0 to skip): "))
                if choice == 0:
                    break
                    
                location = available[choice-1]
                self.locations[location] = True
                available.remove(location)
                self.handle_location(location)
            
            self.current_day += 1
            self.locations = {k: False for k in self.locations}
        
        print("\nGame Over!")
        print(f"Final Affection: {self.affection}")
        print(self.get_ending())

if __name__ == "__main__":
    game = Game()
    game.play()