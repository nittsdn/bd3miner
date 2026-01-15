# BD3MINER - Borderlands 3 Item/Object Class ID Scanner
# Mục đích: Hiện tên Class chính xác của bất cứ thứ gì bạn nhìn hoặc chạm vào.

import unrealsdk
from unrealsdk import logging
from mods_base import build_mod, hook
from unrealsdk.unreal import UObject, WrappedStruct, BoundFunction
from typing import Any
import os
import traceback
from datetime import datetime
from pathlib import Path

# ====================
# LOGGING SYSTEM
# ====================

# Tạo đường dẫn log file trong thư mục user
LOG_DIR = Path.home() / "Documents" / "My Games" / "Borderlands 3" / "Logs"
LOG_FILE = LOG_DIR / "bd3miner.log"

# Tạo thư mục nếu chưa có
try:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_initialized = True
except Exception as e:
    log_initialized = False
    logging.error(f"[BD3MINER] Cannot create log directory: {e}")

def write_log(msg, level="INFO"):
    """Ghi log ra file và console"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] [{level}] {msg}\n"
    
    # Ghi ra console
    if level == "ERROR":
        logging.error(f"[BD3MINER] {msg}")
    elif level == "WARNING":
        logging.warning(f"[BD3MINER] {msg}")
    else:
        logging.info(f"[BD3MINER] {msg}")
    
    # Ghi ra file
    if log_initialized:
        try:
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(log_line)
        except Exception as e:
            logging.error(f"[BD3MINER] Cannot write to log file: {e}")

def inspect_log(msg):
    """Hiển thị thông tin inspector (console + màn hình + file)"""
    write_log(msg, "INFO")
    
    # In lên màn hình chat để dễ thấy
    try:
        pc = unrealsdk.get_player_controller()
        if pc:
            pc.ClientMessage(f"[BD3MINER] {msg}", "Event", True)
    except Exception as e:
        write_log(f"Error showing message on screen: {e}", "ERROR")

# ====================
# HOOKS
# ====================

# Hook: Soi Item dưới đất (Khi nhìn vào)
@hook("/Script/GbxInventory.InventoryItemPickup:OnLookedAtByPlayer")
def on_look_at_item(obj: UObject, args: WrappedStruct, ret: Any, func: BoundFunction):
    """Hook được gọi khi player nhìn vào item dưới đất"""
    try:
        write_log("=== ITEM LOOKED AT HOOK TRIGGERED ===", "INFO")
        
        # Lấy tên hiển thị
        try:
            visible_name = str(obj.InventoryName) if hasattr(obj, 'InventoryName') else "Unknown"
            write_log(f"Item visible name: {visible_name}", "INFO")
        except Exception as e:
            visible_name = "Unknown Item"
            write_log(f"Error getting visible name: {e}", "ERROR")

        # Lấy Class Path
        try:
            full_class_name = obj.Class.get_full_name()
            write_log(f"Item class name: {full_class_name}", "INFO")
        except Exception as e:
            full_class_name = "Unknown Class"
            write_log(f"Error getting class name: {e}", "ERROR")
        
        # Lấy object name
        try:
            obj_name = obj.get_name()
            write_log(f"Item object name: {obj_name}", "INFO")
        except Exception as e:
            write_log(f"Error getting object name: {e}", "ERROR")

        # Hiển thị thông tin
        inspect_log(f"ITEM SEEN: {visible_name}")
        inspect_log(f"CLASS: {full_class_name}")
        
    except Exception as e:
        write_log(f"Critical error in on_look_at_item: {e}", "ERROR")
        write_log(traceback.format_exc(), "ERROR")

# Hook: Soi Hòm/Tủ (Khi bấm mở)
@hook("/Script/OakGame.OakInteractiveObject:OnUsedBy")
def on_use_object(obj: UObject, args: WrappedStruct, ret: Any, func: BoundFunction):
    """Hook được gọi khi player sử dụng object (mở hòm, tủ, v.v.)"""
    try:
        write_log("=== OBJECT USED HOOK TRIGGERED ===", "INFO")
        
        # Lấy tên Object
        try:
            obj_name = obj.get_name()
            write_log(f"Object name: {obj_name}", "INFO")
        except Exception as e:
            obj_name = "Unknown Object"
            write_log(f"Error getting object name: {e}", "ERROR")
        
        # Lấy Class Path
        try:
            full_class_name = obj.Class.get_full_name()
            write_log(f"Object class: {full_class_name}", "INFO")
        except Exception as e:
            full_class_name = "Unknown Class"
            write_log(f"Error getting class name: {e}", "ERROR")
        
        # Thông tin thêm về object
        try:
            obj_type = type(obj).__name__
            write_log(f"Object type: {obj_type}", "INFO")
        except Exception as e:
            write_log(f"Error getting object type: {e}", "ERROR")

        # Hiển thị thông tin
        inspect_log(f"OBJECT USED: {obj_name}")
        inspect_log(f"CLASS: {full_class_name}")
        
    except Exception as e:
        write_log(f"Critical error in on_use_object: {e}", "ERROR")
        write_log(traceback.format_exc(), "ERROR")

# ====================
# MOD INITIALIZATION
# ====================

# Build Mod
mod = build_mod(
    name="bd3miner",
    author="User & AI",
    description="Item/Object Class ID Scanner with detailed logging. Check log at: " + str(LOG_FILE),
    version="1.0"
)

# Log khởi động
write_log("=" * 80, "INFO")
write_log("BD3MINER MOD INITIALIZED", "INFO")
write_log(f"Log file location: {LOG_FILE}", "INFO")
write_log(f"Log directory exists: {LOG_DIR.exists()}", "INFO")
write_log(f"Log file writable: {log_initialized}", "INFO")
write_log("Hooks registered:", "INFO")
write_log("  - /Script/GbxInventory.InventoryItemPickup:OnLookedAtByPlayer", "INFO")
write_log("  - /Script/OakGame.OakInteractiveObject:OnUsedBy", "INFO")
write_log("=" * 80, "INFO")
write_log("", "INFO")
write_log("MOD READY! Look at items or open objects to scan them.", "INFO")
write_log("Press F6 to open console for real-time logs.", "INFO")
write_log("", "INFO")

logging.info(f"[BD3MINER] MOD READY! Log file: {LOG_FILE}")
