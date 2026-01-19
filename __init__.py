import unrealsdk
from unrealsdk.hooks import add_hook, Type
from mods_base import build_mod, hook, get_pc
from unrealsdk.unreal import UObject, WrappedStruct, BoundFunction
from typing import Any
from pathlib import Path
from datetime import datetime
import traceback
import os

__version__ = "1.2.0"

# === LOGGING IN MOD FOLDER ===
MOD_DIR = Path(__file__).parent
LOG_DIR = MOD_DIR / "logs"
LOG_FILE = LOG_DIR / "bd3miner.log"

try:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_initialized = True
except Exception as e:
    log_initialized = False
    print(f"[BD3MINER] Cannot create log directory: {e}")

def write_log(msg, level="INFO"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    log_line = f"[{timestamp}] [{level:8s}] {msg}\n"
    try:
        print(f"[BD3MINER][{level}] {msg}")
        if log_initialized:
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(log_line)
    except Exception as e:
        print(f"[BD3MINER] Logging error: {e}")

# === HOOK: Log khi vũ khí (weapon pickup) Spawn trên map ===
WEAPON_PICKUP_CLASS = "BP_OakWeaponPickup_C"

def log_weapon_beginplay(obj, args, ret, func):
    try:
        # Try lấy location nếu có
        loc = getattr(obj, "K2_GetActorLocation", lambda: None)()
        msg = f"[MAGNET][BeginPlay] {getattr(obj.Class, 'Name', '')} | loc={str(loc) if loc else 'unknown'}"
        write_log(msg, "INFO")
    except Exception as e:
        write_log(f"[MAGNET][BeginPlay][ERR] {e}", "ERROR")
    return False

try:
    add_hook(f"/Game/Pickups/ItemPickups/{WEAPON_PICKUP_CLASS}:{'ReceiveBeginPlay'}", Type.POST, "bd3miner_weapon_pickup_beginplay", log_weapon_beginplay)
    write_log(f"✅ Hooked BeginPlay for {WEAPON_PICKUP_CLASS}", "INFO")
except Exception as e:
    write_log(f"❌ Failed to hook BeginPlay for {WEAPON_PICKUP_CLASS}: {e}", "ERROR")


# === 2 Hook mẫu cơ bản: nhìn item & mở hòm/tủ ===

@hook("/Script/GbxInventory.InventoryItemPickup:OnLookedAtByPlayer")
def on_look_at_item(obj: UObject, args: WrappedStruct, ret: Any, func: BoundFunction):
    try:
        write_log("=== ITEM LOOKED AT HOOK TRIGGERED ===")
        visible_name = str(getattr(obj, "InventoryName", "Unknown"))
        try:
            class_name = getattr(obj.Class, "GetName", lambda: str(obj.Class))()
        except Exception:
            class_name = str(obj.Class)
        write_log(f"Item visible name: {visible_name}")
        write_log(f"Item class name: {class_name}")
        write_log(f"Item object name: {str(getattr(obj.Class, 'Name', ''))}")
    except Exception as e:
        write_log(f"Critical error in on_look_at_item: {e}", "ERROR")
        write_log(traceback.format_exc())

@hook("/Script/OakGame.OakInteractiveObject:OnUsedBy")
def on_use_object(obj: UObject, args: WrappedStruct, ret: Any, func: BoundFunction):
    try:
        write_log("=== OBJECT USED HOOK TRIGGERED ===")
        obj_name = str(getattr(obj.Class, 'Name', 'Unknown Object'))
        class_name = getattr(obj.Class, "GetName", lambda: str(obj.Class))()
        write_log(f"Object name: {obj_name}")
        write_log(f"Object class: {class_name}")
    except Exception as e:
        write_log(f"Critical error in on_use_object: {e}", "ERROR")
        write_log(traceback.format_exc())

# === MOD INIT ===
write_log("="*75, "INFO")
write_log(f"BD3MINER {__version__} STARTUP, Logging to {LOG_FILE.absolute()}", "INFO")

mod = build_mod(
    name="bd3miner", 
    version=__version__,
    description="BL3 item/object miner with weapon BeginPlay hook"
)