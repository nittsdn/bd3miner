# BD3MINER - Borderlands 3 Item/Object Class ID Scanner
# Version 1.1.0 - ProcessEvent Hook Research Edition
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

__version__ = "1.1.0"

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
    """Enhanced logging with timestamp and categorization"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    log_line = f"[{timestamp}] [{level:8s}] {msg}\n"
    
    # Console output with color coding
    if level == "ERROR":
        logging.error(f"[BD3MINER] {msg}")
    elif level == "WARNING":
        logging.warning(f"[BD3MINER] {msg}")
    elif level == "DEBUG":
        try:
            logging.dev_warning(f"[BD3MINER] {msg}")
        except AttributeError:
            # dev_warning might not exist in all versions
            logging.info(f"[BD3MINER] [DEBUG] {msg}")
    else:
        logging.info(f"[BD3MINER] {msg}")
    
    # File output
    if log_initialized:
        try:
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(log_line)
        except Exception as e:
            logging.error(f"[BD3MINER] Cannot write to log: {e}")

def log_separator(title=""):
    """Add visual separator in logs"""
    separator = "=" * 80
    write_log(separator, "INFO")
    if title:
        write_log(f"  {title}", "INFO")
        write_log(separator, "INFO")

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

def log_event(event_type, obj, func, extra_info=""):
    """Standardized event logging"""
    try:
        obj_class = obj.Class.get_full_name() if hasattr(obj, 'Class') else "Unknown"
        obj_name = obj.get_name() if obj else "Unknown"
        func_name = func.get_full_name() if func else "Unknown"
        
        write_log("", "INFO")  # Empty line for readability
        write_log(f"EVENT CAPTURED: {event_type}", "INFO")
        write_log(f"  Object Class: {obj_class}", "INFO")
        write_log(f"  Object Name: {obj_name}", "INFO")
        write_log(f"  Function: {func_name}", "INFO")
        if extra_info:
            write_log(f"  Extra: {extra_info}", "INFO")
        write_log("", "INFO")
        
    except Exception as e:
        write_log(f"Error logging event: {e}", "ERROR")

# ====================
# API DISCOVERY
# ====================

def discover_apis():
    """Discover and log available APIs at startup"""
    log_separator("API DISCOVERY PHASE")
    
    write_log(f"unrealsdk module contents: {dir(unrealsdk)}", "INFO")
    
    if hasattr(unrealsdk, 'hooks'):
        write_log(f"unrealsdk.hooks contents: {dir(unrealsdk.hooks)}", "INFO")
    else:
        write_log("unrealsdk.hooks not found", "WARNING")
    
    if hasattr(unrealsdk, 'hook_manager'):
        write_log(f"unrealsdk.hook_manager contents: {dir(unrealsdk.hook_manager)}", "INFO")
    else:
        write_log("unrealsdk.hook_manager not found", "INFO")
    
    try:
        from unrealsdk.hooks import add_hook, remove_hook
        write_log("✅ Low-level hook API (add_hook) is available!", "INFO")
        return True
    except ImportError as e:
        write_log(f"❌ Low-level hook API not available: {e}", "ERROR")
    except Exception as e:
        write_log(f"❌ Error checking low-level hook API: {e}", "ERROR")
    
    try:
        import pyunrealsdk
        write_log(f"✅ pyunrealsdk available: {dir(pyunrealsdk)}", "INFO")
    except ImportError:
        write_log("ℹ️ pyunrealsdk not directly importable", "INFO")
    
    return False

# ====================
# PROCESSEVENT HOOK (TIER 1)
# ====================

def try_process_event_hook():
    """Attempt to hook ProcessEvent directly"""
    try:
        from unrealsdk.hooks import add_hook, Type
        
        def process_event_inspector(obj, args, ret, func):
            """Intercept ALL ProcessEvent calls"""
            try:
                # Get function and object names
                func_name = func.get_full_name() if func else "Unknown"
                obj_name = obj.get_full_name() if obj else "Unknown"
                
                # Filter - only log events related to Inventory/Bank/UI/Item
                keywords = ["Inventory", "Bank", "UI", "Item", "Pickup", "Weapon", "Shield", "Oak"]
                if any(keyword in obj_name or keyword in func_name for keyword in keywords):
                    write_log(f"PROCESSEVENT: {obj_name} → {func_name}", "INFO")
                
            except Exception as e:
                write_log(f"Error in process_event_inspector: {e}", "ERROR")
            
            return False  # Allow function to continue
        
        # Try multiple ProcessEvent paths
        for attempt_path in ["ProcessEvent", "UObject:ProcessEvent", "UObject::ProcessEvent"]:
            try:
                add_hook(attempt_path, Type.PRE, "bd3miner_inspector", process_event_inspector)
                write_log(f"✅ SUCCESS! Hooked ProcessEvent via: {attempt_path}", "INFO")
                return True
            except Exception as e:
                write_log(f"❌ Failed to hook '{attempt_path}': {e}", "WARNING")
        
        return False
        
    except Exception as e:
        write_log(f"❌ ProcessEvent hook completely failed: {e}", "ERROR")
        return False

# ====================
# MULTI-HOOK FALLBACK (TIER 2)
# ====================

IMPORTANT_HOOKS = [
    "/Script/OakGame.OakPlayerController:ServerInventoryItemSort",
    "/Script/OakGame.OakInventoryManager:TransferItem",
    "/Script/OakGame.OakInventoryManager:AddInventoryItem",
    "/Script/OakGame.OakInventoryManager:RemoveInventoryItem",
    "/Script/OakGame.OakBankInventoryComponent:DepositItem",
    "/Script/OakGame.OakBankInventoryComponent:WithdrawItem",
    "/Script/GbxInventory.InventoryItemPickup:OnLookedAtByPlayer",
    "/Script/GbxInventory.InventoryItemPickup:OnPickedUp",
    "/Script/OakGame.OakInteractiveObject:OnUsedBy",
    "/Script/OakGame.OakUIInventoryMenu:OnOpened",
    "/Script/OakGame.OakUIInventoryMenu:OnClosed",
]

def setup_multi_hook_fallback():
    """Setup multiple specific hooks as fallback"""
    write_log("=== FALLBACK: Setting up multi-hook approach ===", "INFO")
    
    success_count = 0
    for hook_path in IMPORTANT_HOOKS:
        try:
            # Create a closure to capture hook_path
            def make_handler(path):
                def multi_hook_handler(obj: UObject, args: WrappedStruct, ret: Any, func: BoundFunction):
                    try:
                        obj_name = obj.get_full_name() if obj else "Unknown"
                        func_name = func.get_full_name() if func else "Unknown"
                        write_log(f"MULTI-HOOK [{path}]: {obj_name} → {func_name}", "INFO")
                        log_event(path, obj, func)
                    except Exception as e:
                        write_log(f"Error in multi_hook_handler for {path}: {e}", "ERROR")
                return multi_hook_handler
            
            # Register the hook
            hook(hook_path, "POST")(make_handler(hook_path))
            write_log(f"✅ Registered hook: {hook_path}", "DEBUG")
            success_count += 1
        except Exception as e:
            write_log(f"❌ Failed to register hook {hook_path}: {e}", "WARNING")
    
    write_log(f"Multi-hook setup complete: {success_count}/{len(IMPORTANT_HOOKS)} successful", "INFO")

# ====================
# ORIGINAL HOOKS (Always Active)
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
        
        # Log event with standardized format
        log_event("ITEM_LOOKED_AT", obj, func, f"Visible name: {visible_name}")
        
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
        
        # Log event with standardized format
        log_event("OBJECT_USED", obj, func)
        
    except Exception as e:
        write_log(f"Critical error in on_use_object: {e}", "ERROR")
        write_log(traceback.format_exc(), "ERROR")

# ====================
# MOD INITIALIZATION
# ====================

# Mod startup sequence
log_separator("BD3MINER MOD STARTING")
write_log(f"Version: {__version__}", "INFO")
write_log(f"Log file: {LOG_FILE}", "INFO")
write_log(f"Log directory exists: {LOG_DIR.exists()}", "INFO")

# API Discovery Phase
has_low_level_api = discover_apis()

# Hook Setup Phase
log_separator("HOOK SETUP PHASE")

# Always set up original hooks (they're registered via decorators)
write_log("Original hooks are active:", "INFO")
write_log("  ✅ /Script/GbxInventory.InventoryItemPickup:OnLookedAtByPlayer", "INFO")
write_log("  ✅ /Script/OakGame.OakInteractiveObject:OnUsedBy", "INFO")

# Try ProcessEvent hook if API is available
if has_low_level_api:
    if try_process_event_hook():
        write_log("🎉 Using ProcessEvent hook (BEST)", "INFO")
    else:
        write_log("⚠️ ProcessEvent hook failed, using fallback", "WARNING")
        setup_multi_hook_fallback()
else:
    write_log("⚠️ Low-level API not available, using fallback", "WARNING")
    setup_multi_hook_fallback()

# Build Mod
mod = build_mod(
    name="bd3miner",
    author="User & AI",
    description="Item/Object Class ID Scanner with ProcessEvent hooks. Log: " + str(LOG_FILE),
    version=__version__
)

# Final startup message
log_separator("BD3MINER READY")
write_log("Mod is active! Check console (F6) and this log file", "INFO")
write_log("", "INFO")
write_log("=== USER INSTRUCTIONS ===", "INFO")
write_log("1. Look at items on the ground to scan them", "INFO")
write_log("2. Open chests/objects to scan them", "INFO")
write_log("3. Open/close inventory to trigger hooks", "INFO")
write_log("4. Move items to/from bank to trigger hooks", "INFO")
write_log("5. Check this log file for detailed information", "INFO")
write_log("6. Press F6 to see console output in real-time", "INFO")
write_log("", "INFO")
write_log("If you see 'ProcessEvent hook' messages above, the advanced hook is working!", "INFO")
write_log("If you see 'FALLBACK' messages, the mod is using backup hooks (still works!)", "INFO")
write_log("", "INFO")

logging.info(f"[BD3MINER] MOD READY! Version {__version__} - Log file: {LOG_FILE}")
