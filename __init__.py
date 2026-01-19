"""
bd3miner v1.3.1-magnet-snoop POST+ProcessEvent
Last updated: 2026-01-20 00:03
Sniff mọi event, cả PRE & POST, cả ProcessEvent trên tất cả Pickup class!
"""
import unrealsdk
from unrealsdk.hooks import add_hook, Type
from mods_base import build_mod
from pathlib import Path
from datetime import datetime
import os

__version__ = "1.3.1-magnet-snoop"
MOD_DIR = Path(__file__).parent
LOG_DIR = MOD_DIR / "logs"
LOG_FILE = LOG_DIR / "bd3miner.log"
LOG_DIR.mkdir(parents=True, exist_ok=True)

def write_log(msg, level="INFO"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    log_line = f"[{timestamp}] [{level:8s}] {msg}\n"
    print(f"[BD3MINER][{level}] {msg}")
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_line)
    except Exception as e:
        print(f"[BD3MINER] Logging error: {e}")

PICKUP_CLASSES = [
    "BP_OakConsumableItemPickup_C", "BP_OakInventoryItemPickup_Ammo_C", "BP_OakInventoryItemPickup_Shield_C",
    "BP_OakInventoryItemPickup_C", "BP_OakInventoryItemPickup_Classmod_C", "BP_OakInventoryItemPickup_GrenadeMod_C",
    "BP_OakInventoryItemPickup_Artifact_C", "BP_OakWeaponPickup_C", "BP_OakInventoryItemPickup_Eridium_C"
]
AUTO_PICKUP_FUNCS = [
    "TryActivatePickup", "OnTouched", "OnAutoCollected", "ReceiveActorBeginOverlap",
    "NotifyActorBeginOverlap", "OnPickedUp", "OnHealthPickedUp", "OnAmmoPickedUp",
    "OnShieldPickedUp", "ShowLootBeam"
]

def magnet_logger(obj, args, ret, func):
    try:
        msg = f"[MAGNET_TRACK][PRE] {func.Name} | caller: {obj} | class: {getattr(obj, 'Class', None)}"
        write_log(msg, "INFO")
    except Exception as e:
        write_log(f"[MAGNET_TRACK][PRE][ERR] {e}", "ERROR")
def magnet_logger_post(obj, args, ret, func):
    try:
        msg = f"[MAGNET_TRACK][POST] {func.Name} | caller: {obj} | class: {getattr(obj, 'Class', None)}"
        write_log(msg, "INFO")
    except Exception as e:
        write_log(f"[MAGNET_TRACK][POST][ERR] {e}", "ERROR")

# Hook cả PRE và POST lên mọi func magnet trên các Pickup class
for class_name in PICKUP_CLASSES:
    for func_name in AUTO_PICKUP_FUNCS:
        try:
            hook_path = f"/Game/Pickups/_Shared/_Design/{class_name}:{func_name}"
            add_hook(hook_path, Type.PRE, f"magnetlogpre_{class_name}_{func_name}", magnet_logger)
            add_hook(hook_path, Type.POST, f"magnetlogpost_{class_name}_{func_name}", magnet_logger_post)
        except Exception as e:
            write_log(f"❌ Fail-{class_name}:{func_name}: {e}", "ERROR")

# Hook ProcessEvent toàn bộ Pickup class để sniff mọi event
def process_event_sniff(obj, func, args):
    try:
        if hasattr(obj, "Class") and any(cls in str(obj.Class.Name) for cls in PICKUP_CLASSES):
            msg = f"[MAGNET_TRACK][ProcessEvent] Obj: {obj.Class.Name} | Func: {func.Name}"
            write_log(msg, "INFO")
    except Exception as e:
        write_log(f"[MAGNET_TRACK][ProcessEvent][ERR] {e}", "ERROR")
    return True

for class_name in PICKUP_CLASSES:
    try:
        hook_path = f"/Game/Pickups/_Shared/_Design/{class_name}:ProcessEvent"
        add_hook(hook_path, Type.PRE, f"processevent_{class_name}", process_event_sniff)
    except Exception as e:
        write_log(f"❌ Fail-ProcessEvent-{class_name}: {e}", "ERROR")

write_log("="*75, "INFO")
write_log(f"BD3MINER {__version__} SNIFFER ACTIVE - Logging magnet events PRE + POST + ProcessEvent", "INFO")

build_mod(
    name="bd3miner",
    version=__version__,
    description="Log magnet auto-pickup events PRE + POST + ProcessEvent (deep sniff)"
)