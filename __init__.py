# BD3MINER - Borderlands 3 Item/Object Class ID Scanner
# Version 1.1.2 - Phase 1 Runtime Observe (Fixed)
# Mục tiêu: Quan sát và log events RAW theo spec P1 (fixed hooks).

import unrealsdk
from unrealsdk import logging
from mods_base import build_mod, hook, get_pc
from unrealsdk.unreal import UObject, WrappedStruct, BoundFunction
from typing import Any
import os
import traceback
from datetime import datetime
from pathlib import Path
import json

__version__ = "1.1.2"

# ====================
# LOGGING SYSTEM (JSON Lines for P1)
# ====================

# File log P1: bd3_runtime.log.jsonl (append-only)
LOG_DIR = Path(__file__).parent / "logs"
RUNTIME_LOG_FILE = LOG_DIR / "bd3_runtime.log.jsonl"

# Tạo thư mục
try:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    with open(RUNTIME_LOG_FILE, "a", encoding="utf-8") as f:
        f.write("")  # Test write
    logging.info(f"[BD3MINER] Log file ready: {RUNTIME_LOG_FILE}")
except Exception as e:
    logging.error(f"[BD3MINER] Cannot create log file: {e}")

def log_event_jsonl(event_type, actor_class=None, actor_id=None, instigator_type="Player", instigator_id="Player_0", context_map=None, extra_note=None):
    """Log RAW event in JSON Lines format (P1 spec)"""
    try:
        # Safe get data (default if not available)
        ts = 0.0
        try:
            ts = unrealsdk.GetGameTimeSeconds()
        except AttributeError:
            pass
        
        frame = 0
        try:
            frame = unrealsdk.GetFrameNumber()
        except AttributeError:
            pass
        
        map_name = "Unknown"
        try:
            map_name = unrealsdk.GetCurrentLevelName() or "Unknown"
        except AttributeError:
            pass
        
        # Build JSON
        log_entry = {
            "ts": float(ts),
            "frame": int(frame),
            "event": event_type,
            "actor": {
                "class": actor_class or "Unknown",
                "id": actor_id or "0x0"
            },
            "instigator": {
                "type": instigator_type,
                "id": instigator_id
            },
            "context": {
                "map": map_name,
                "area": None,
                "mode": None
            },
            "extra": {
                "note": extra_note
            }
        }
        
        # Append to file
        with open(RUNTIME_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")
        
        # Console log
        logging.info(f"[BD3MINER] Logged: {event_type}")
        
    except Exception as e:
        logging.error(f"[BD3MINER] Log error: {e}")

# ====================
# PHASE 1 HOOKS (Fixed paths)
# ====================

# Hook: Actor spawn (fixed path)
@hook("/Script/Engine.Actor:ReceiveBeginPlay")
def on_actor_spawned(obj: UObject, args: WrappedStruct, ret: Any, func: BoundFunction):
    """Log khi actor spawn"""
    try:
        actor_class = str(obj.Class.Name) if hasattr(obj, 'Class') and hasattr(obj.Class, 'Name') else "Unknown"
        actor_id = str(hex(id(obj)))
        log_event_jsonl("ActorSpawned", actor_class=actor_class, actor_id=actor_id)
    except Exception as e:
        logging.error(f"[BD3MINER] Hook ReceiveBeginPlay error: {e}")

# Hook: Player pickup item
@hook("/Script/GbxInventory.InventoryItemPickup:OnPickedUp")
def on_pickup(obj: UObject, args: WrappedStruct, ret: Any, func: BoundFunction):
    """Log khi player pickup"""
    try:
        actor_class = str(obj.Class.Name) if hasattr(obj, 'Class') and hasattr(obj.Class, 'Name') else "Unknown"
        actor_id = str(hex(id(obj)))
        log_event_jsonl("Pickup", actor_class=actor_class, actor_id=actor_id)
    except Exception as e:
        logging.error(f"[BD3MINER] Hook OnPickedUp error: {e}")

# Hook: Actor destroyed (fixed path)
@hook("/Script/Engine.Actor:K2_DestroyActor")
def on_destroyed(obj: UObject, args: WrappedStruct, ret: Any, func: BoundFunction):
    """Log khi actor destroy"""
    try:
        actor_class = str(obj.Class.Name) if hasattr(obj, 'Class') and hasattr(obj.Class, 'Name') else "Unknown"
        actor_id = str(hex(id(obj)))
        log_event_jsonl("ActorDestroyed", actor_class=actor_class, actor_id=actor_id)
    except Exception as e:
        logging.error(f"[BD3MINER] Hook K2_DestroyActor error: {e}")

# Hook: Input key
@hook("/Script/Engine.PlayerController:InputKey")
def on_input_key(obj: UObject, args: WrappedStruct, ret: Any, func: BoundFunction):
    """Log key input"""
    try:
        if hasattr(args, 'Key') and hasattr(args.Key, 'KeyName') and str(args.Key.KeyName) == "F6":
            log_event_jsonl("InputKey", extra_note="F6 pressed")
    except Exception as e:
        logging.error(f"[BD3MINER] Hook InputKey error: {e}")

# ====================
# MOD INITIALIZATION
# ====================

# Startup check
logging.info("[BD3MINER] Mod loaded - Phase 1 Runtime Observe")

mod = build_mod(
    name="bd3miner",
    author="User & AI",
    description="P1 Runtime Observe: Log RAW events to bd3_runtime.log.jsonl.",
    version=__version__
)