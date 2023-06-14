import random
import numpy as np
from fpdf import FPDF

class Character:
    def __init__(self, name, goal, char_class, level):
        self.name = name
        self.goal = goal
        self.char_class = char_class
        self.level = level
        self.attributes = self.roll_attributes()
        self.modifiers = self.calculate_modifiers()
        self.skills = self.generate_skills()
        self.hit_points = self.roll_hit_points()
        self.attack_bonus = self.calculate_attack_bonus()
        self.foci = self.select_foci()
        self.equipment = self.select_equipment()
        self.armor_class = self.calculate_armor_class()
        self.saving_throws = self.calculate_saving_throws()

    def roll_attributes(self):
        attributes = ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]
        attr_values = [random.randint(1, 6) + random.randint(1, 6) + random.randint(1, 6) for _ in range(6)]
        attr_values.sort()
        attr_values[0] = 14  # Set the lowest roll to 14
        random.shuffle(attr_values)  # Shuffle the values before assigning
        return {attr: value for attr, value in zip(attributes, attr_values)}

    def calculate_modifiers(self):
        modifiers = {}
        for attr, value in self.attributes.items():
            if value <= 3:
                modifiers[attr] = -2
            elif value <= 7:
                modifiers[attr] = -1
            elif value <= 13:
                modifiers[attr] = 0
            elif value <= 17:
                modifiers[attr] = 1
            else:
                modifiers[attr] = 2
        return modifiers

    def generate_skills(self):
        base_skills = ["Pilot", "Shoot", "Exert", "Connect", "Notice", "Perform", "Program", "Punch", "Survive", "Trade", "Work"]
        chosen_skills = np.random.choice(base_skills, size=5, replace=False)
        skill_levels = {skill: 0 for skill in chosen_skills}
        print("LEVEL", self.level)
        for _ in range(self.level):
            skill_to_increment = np.random.choice(list(skill_levels.keys()))
            skill_levels[skill_to_increment] += 1

        return skill_levels

    def roll_hit_points(self):
        base_hp = (self.level - 1) * np.random.randint(1, 7)
        level_hp = (self.level - 1) * np.random.randint(1, 7)  # Roll a d6 for additional HP for each level beyond 1
        hp_bonus = 0
        if self.char_class in ["Warrior", "Adventurer"]:
            hp_bonus = 2
        return max(1, base_hp + level_hp + hp_bonus + self.modifiers["Constitution"])


    def calculate_attack_bonus(self):
        return 0 if self.char_class != "Warrior" else 1

    def select_foci(self):
        all_foci = ["Specialist", "Alert", "Connected", "Ironhide", "Gunslinger", "Close Combatant"]
        return np.random.choice(all_foci)

    def select_equipment(self):
        equipment_packages = [
            ["Laser Rifle", "Combat Field Uniform", "Monoblade", "Lazarus Patch", "Rations (1 week)"],
            ["Mag Pistol", "Secure Clothing", "Monoblade", "Lazarus Patch", "Rations (1 week)"],
            ["Stun Baton", "Secure Clothing", "Monoblade", "Lazarus Patch", "Rations (1 week)"],
            ["Laser Pistol", "Secure Clothing", "Monoblade", "Lazarus Patch", "Rations (1 week)"]
        ]
        return random.choice(equipment_packages)

    def calculate_armor_class(self):
        return 10 + self.modifiers["Dexterity"]

    def calculate_saving_throws(self):
        physical_save = 15 - max(self.modifiers["Strength"], self.modifiers["Constitution"])
        evasion_save = 15 - max(self.modifiers["Intelligence"], self.modifiers["Dexterity"])
        mental_save = 15 - max(self.modifiers["Wisdom"], self.modifiers["Charisma"])
        return {"Physical": physical_save, "Evasion": evasion_save, "Mental": mental_save}

    def to_pdf(self, filename):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Name: {self.name}", ln=True)
        pdf.cell(200, 10, txt=f"Goal: {self.goal}", ln=True)
        pdf.cell(200, 10, txt=f"Class: {self.char_class}", ln=True)
        pdf.cell(200, 10, txt=f"Level: {self.level}", ln=True)
        for attr, value in self.attributes.items():
            pdf.cell(200, 10, txt=f"{attr}: {value} (modifier: {self.modifiers[attr]})", ln=True)
        pdf.cell(200, 10, txt=f"Hit Points: {self.hit_points}", ln=True)
        pdf.cell(200, 10, txt=f"Attack Bonus: {self.attack_bonus}", ln=True)
        pdf.cell(200, 10, txt="Skills:", ln=True)
        for skill, level in self.skills.items():
          pdf.cell(200, 10, txt=f"{skill}: {level}", ln=True)
        pdf.cell(200, 10, txt=f"Focus: {self.foci}", ln=True)
        pdf.cell(200, 10, txt=f"Equipment: {', '.join(self.equipment)}", ln=True)
        pdf.cell(200, 10, txt=f"Armor Class: {self.armor_class}", ln=True)
        for save, value in self.saving_throws.items():
            pdf.cell(200, 10, txt=f"{save} Saving Throw: {value}", ln=True)
        pdf.output(filename)

def generate_npc(name, goal, char_class=None, level=1):
    if char_class is None:
        char_class = np.random.choice(["Warrior", "Expert", "Psychic", "Adventurer"])
    npc = Character(name, goal, char_class, level)
    npc.to_pdf("characters/" + f"{name}.pdf")

def main():
    name = input("Enter character name: ")
    goal = input("Enter character goal: ")
    char_class = input("Enter character class (Warrior, Expert, Psychic, Adventurer) or leave it empty for random: ")
    if char_class == "":
        char_class = None
    level = input("Enter character level or leave it empty for default level (1): ")
    if level == "":
        level = 1
    else:
        level = int(level)
    print("INPUT:", name, goal, char_class, level)
    generate_npc(name, goal, char_class, level)

# Run the main function
if __name__ == "__main__":
    main()