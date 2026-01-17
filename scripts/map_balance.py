import json

# Load clean log file
log_file = '../logs/bd3_runtime_clean.log.jsonl'
classes = set()

with open(log_file, 'r') as f:
    for line in f:
        data = json.loads(line.strip())
        classes.add(data['actor']['class'])

# Placeholder mapping (update manually with save editor)
class_to_balance = {}
for cls in sorted(classes):
    # Placeholder paths - replace with actual from save editor
    if 'Consumable' in cls:
        class_to_balance[cls] = '/Game/Gear/Consumables/Placeholder'
    elif 'Shield' in cls:
        class_to_balance[cls] = '/Game/Gear/Shields/Placeholder'
    elif 'Classmod' in cls:
        class_to_balance[cls] = '/Game/Gear/ClassMods/Placeholder'
    elif 'GrenadeMod' in cls:
        class_to_balance[cls] = '/Game/Gear/GrenadeMods/Placeholder'
    elif 'Weapon' in cls:
        class_to_balance[cls] = '/Game/Gear/Weapons/Placeholder'
    else:
        class_to_balance[cls] = '/Unknown/Placeholder'

# Save mapping
with open('../data/class_to_balance.json', 'w') as f:
    json.dump(class_to_balance, f, indent=2)

print(f"Mapped {len(classes)} classes to placeholders. Update manually with save editor.")