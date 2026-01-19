"""
bd3miner v1.3.0-magnet-snoop
Last updated: 2026-01-19 23:55
Mục tiêu: Log mọi event hút máu/đạn/shield - sniff auto pickup magnet cơ chế ngầm BL3
"""
import unrealsdk
from unrealsdk.hooks import add_hook, Type
from mods_base import build_mod, hook, get_pc
from unrealsdk.unreal import UObject, WrappedStruct, BoundFunction
from pathlib import Path
from datetime import datetime
import traceback
import os

__version__ = "1.3.0-magnet-snoop"
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

# List các pickup class thường thấy (ammo, health, shield, consumable)
PICKUP_CLASSES = [
    "BP_OakConsumableItemPickup_C",
    "BP_OakInventoryItemPickup_Ammo_C",
    "BP_OakInventoryItemPickup_Shield_C",
    "BP_OakInventoryItemPickup_C",           # generic
    "BP_OakInventoryItemPickup_Classmod_C",
    "BP_OakInventoryItemPickup_GrenadeMod_C",
    "BP_OakInventoryItemPickup_Artifact_C",
    "BP_OakWeaponPickup_C",
    "BP_OakInventoryItemPickup_Eridium_C"
]

# Những function phổ biến liên quan auto-pickup, magnet hút
AUTO_PICKUP_FUNCS = [
    "TryActivatePickup", "OnTouched", "OnAutoCollected", "ReceiveActorBeginOverlap",
    "NotifyActorBeginOverlap", "OnPickedUp", "OnHealthPickedUp", "OnAmmoPickedUp",
    "OnShieldPickedUp", "ShowLootBeam"
]

# Helper: Gắn hook vào từng method, log mọi lần gọi, log context
def magnet_logger(obj, args, ret, func):
    try:
        pc = get_pc()
        player_str = str(pc.Pawn) if pc and pc.Pawn else "None"
        msg = f"[MAGNET_TRACK] {func.Name} | caller: {obj} | class: {getattr(obj, 'Class', None)} | player: {player_str}"
        # Dò property động: loại pickup, amount, v.v.
        props = []
        for prop in ["PickupType", "InventoryType", "Amount", "bIsAutoMagnet"]:
            if hasattr(obj, prop):
                props.append(f"{prop}: {getattr(obj, prop)}")
        if props:
            msg += " | " + ", ".join(props)
        write_log(msg, "INFO")
    except Exception as e:
        write_log(f"[MAGNET_TRACK][ERR] {e}", "ERROR")

# Dò mọi func liên quan auto-magnet trên các Pickup class
for class_name in PICKUP_CLASSES:
    for func_name in AUTO_PICKUP_FUNCS:
        try:
            hook_path = f"/Game/Pickups/_Shared/_Design/{class_name}:{func_name}"
            add_hook(hook_path, Type.PRE, f"magnetlog_{class_name}_{func_name}", magnet_logger)
            write_log(f"✅ Hooked {class_name}:{func_name}", "INFO")
        except Exception as e:
            write_log(f"❌ Fail-{class_name}:{func_name}: {e}", "ERROR")

write_log("="*75, "INFO")
write_log(f"BD3MINER {__version__} SNIFFER ACTIVE - Logging magnet events", "INFO")

build_mod(
    name="bd3miner", 
    version=__version__,
    description="Log magnet (auto-pickup) events for ammo/health/shield/gear"
)