import json
from collections import defaultdict

input_file = "bd3_runtime_clean.log.jsonl"  # File clean của bạn

# Counters
class_count = defaultdict(int)
event_count = defaultdict(int)
context_count = defaultdict(lambda: defaultdict(int))  # map -> area -> count

with open(input_file, "r") as f:
    for line in f:
        try:
            data = json.loads(line.strip())
            actor_class = data["actor"]["class"]
            event = data["event"]
            map_name = data["context"]["map"]
            area = data["context"]["area"] or "Unknown"
            
            class_count[actor_class] += 1
            event_count[event] += 1
            context_count[map_name][area] += 1
        except (json.JSONDecodeError, KeyError):
            print(f"Skip invalid line: {line.strip()}")

# Print summary
print("=== CLASS SUMMARY ===")
for cls, cnt in sorted(class_count.items(), key=lambda x: x[1], reverse=True):
    print(f"{cls}: {cnt}")

print("\n=== EVENT SUMMARY ===")
for evt, cnt in sorted(event_count.items(), key=lambda x: x[1], reverse=True):
    print(f"{evt}: {cnt}")

print("\n=== CONTEXT SUMMARY (Map -> Area) ===")
for map_name, areas in context_count.items():
    print(f"Map: {map_name}")
    for area, cnt in sorted(areas.items(), key=lambda x: x[1], reverse=True):
        print(f"  {area}: {cnt}")