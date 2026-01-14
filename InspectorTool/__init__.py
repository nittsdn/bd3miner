# BL3 INSPECTOR TOOL
# Mục đích: Hiện tên Class chính xác của bất cứ thứ gì bạn nhìn hoặc chạm vào.

import unrealsdk
from mods_base import build_mod, hook
from unrealsdk.unreal import UObject, WrappedStruct, BoundFunction
from typing import Any

# 1. Hàm in Log (In ra Console F6)
def inspect_log(msg):
    unrealsdk.Log(f"[INSPECTOR] {msg}")
    # In cả lên màn hình chat để dễ thấy
    pc = unrealsdk.get_player_controller()
    if pc:
        pc.ClientMessage(f"[INSPECT] {msg}", "Event", True)

# 2. Hook: Soi Item dưới đất (Khi nhìn vào)
# Hook vào sự kiện "Item nhận ra nó đang bị nhìn"
@hook("/Script/GbxInventory.InventoryItemPickup:OnLookedAtByPlayer")
def on_look_at_item(obj: UObject, args: WrappedStruct, ret: Any, func: BoundFunction):
    # Lấy tên hiển thị (Ví dụ: "Maggie")
    try:
        visible_name = obj.InventoryName
    except:
        visible_name = "Unknown Item"

    # Lấy Class Path (Cái này quan trọng nhất cho MagnetLoot)
    # Ví dụ: /Game/Gear/Weapons/Pistols/Jakobs/...
    full_class_name = obj.Class.get_full_name()

    inspect_log(f"ITEM SEEN: {visible_name}")
    inspect_log(f"ID: {full_class_name}")

# 3. Hook: Soi Hòm/Tủ (Khi bấm mở)
@hook("/Script/OakGame.OakInteractiveObject:OnUsedBy")
def on_use_object(obj: UObject, args: WrappedStruct, ret: Any, func: BoundFunction):
    # Lấy tên Object
    obj_name = obj.get_name()
    
    # Lấy Class Path (Quan trọng để phân biệt hòm đạn vs hòm Boss)
    full_class_name = obj.Class.get_full_name()

    inspect_log(f"OBJECT USED: {obj_name}")
    inspect_log(f"ID: {full_class_name}")

# 4. Build Mod
mod = build_mod(
    name="InspectorTool",
    author="User & AI",
    description="Look at items or open chests to see their Real ID in Console (F6).",
    version="1.0"
)

unrealsdk.Log("[INSPECTOR] READY! Look at something or Open something.")
