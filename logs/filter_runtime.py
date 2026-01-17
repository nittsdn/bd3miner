import json

# Relevant classes (based on log – pickups, chests, interactive objects)
RELEVANT_CLASSES = [
    "BP_OakConsumableItemPickup_C",
    "BP_OakWeaponPickup_C",
    "BP_OakInventoryItemPickup_Shield_C",
    "BP_OakInventoryItemPickup_Classmod_C",
    "BP_OakInventoryItemPickup_GrenadeMod_C",
    "OakInteractiveObject",  # Chests/containers
    # Add more if you see in log
]

input_file = "bd3_runtime.log.jsonl"
output_file = "bd3_runtime_clean.log.jsonl"

filtered_count = 0
total_count = 0

with open(input_file, "r") as f_in, open(output_file, "w") as f_out:
    for line in f_in:
        total_count += 1
        try:
            data = json.loads(line.strip())
            actor_class = data.get("actor", {}).get("class", "")
            if actor_class in RELEVANT_CLASSES:
                json.dump(data, f_out)
                f_out.write("\n")
                filtered_count += 1
        except json.JSONDecodeError:
            print(f"Skip invalid line: {line.strip()}")

print(f"Total lines: {total_count}")
print(f"Filtered lines: {filtered_count}")
print(f"Output file: {output_file}")