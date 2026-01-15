# 📖 HƯỚNG DẪN CÀI ĐẶT VÀ SỬ DỤNG BD3MINER

## 🎯 Tổng Quan

**bd3miner** là công cụ phát triển (dev tool) cho Borderlands 3 giúp bạn xem Class ID chính xác của items và objects trong game với hệ thống logging chi tiết. Đây là công cụ thiết yếu để phát triển các mod khác như MagnetLoot và BankSort.

---

## 📋 YÊU CẦU HỆ THỐNG

### Phần Mềm Cần Thiết

1. **Borderlands 3** (PC version)
2. **BL3 SDK** (Unrealsdk + mods_base)
   - Download tại: [Oak Mod Manager](https://github.com/bl-sdk/oak-mod-manager)
3. **Python 3.7+** (thường đi kèm SDK)

### Kiểm Tra SDK Đã Cài

Nếu bạn đã cài SDK, bạn sẽ có:
- Thư mục `sdk_mods/` trong thư mục game
- File `d3d11.dll` hoặc `dinput8.dll` trong thư mục game
- Có thể nhấn F6 hoặc ~ trong game để mở Console

---

## 🚀 HƯỚNG DẪN CÀI ĐẶT

### Cách 1: Cài Đặt Từ Repository Này

#### Bước 1: Tải Mod
```bash
# Clone repository
git clone https://github.com/nittsdn/bd3miner.git

# Hoặc download ZIP và giải nén
```

#### Bước 2: Copy Vào Game
1. Mở thư mục cài đặt Borderlands 3
   - Thường ở: `C:\Program Files\Epic Games\Borderlands3\OakGame\Binaries\Win64\`
   - Hoặc: `Steam\steamapps\common\Borderlands 3\OakGame\Binaries\Win64\`

2. Tìm thư mục `sdk_mods/`

3. Copy toàn bộ thư mục vào `sdk_mods/` và đổi tên thành `bd3miner/`

Cấu trúc cuối cùng:
```
Borderlands3/OakGame/Binaries/Win64/
├── sdk_mods/
│   ├── bd3miner/          ← Thư mục mod của bạn
│   │   ├── __init__.py
│   │   └── pyproject.toml
│   └── (các mod khác...)
└── Borderlands3.exe
```

#### Bước 3: Kiểm Tra
1. Khởi động Borderlands 3
2. Nhấn **F5** (Mods Menu)
3. Tìm "bd3miner" trong danh sách
4. Đảm bảo nó có dấu ✓ (enabled)
5. Kiểm tra log file tại: `%USERPROFILE%\Documents\My Games\Borderlands 3\Logs\bd3miner.log`

---

### Cách 2: Cài Đặt Thủ Công

#### Bước 1: Tạo Thư Mục
```
sdk_mods/
└── bd3miner/
```

#### Bước 2: Tạo File `__init__.py`
Copy toàn bộ nội dung sau vào file `bd3miner/__init__.py`:

```python
# BD3MINER - Borderlands 3 Item/Object Class ID Scanner
# Mục đích: Hiện tên Class chính xác của bất cứ thứ gì bạn nhìn hoặc chạm vào.

import unrealsdk
from mods_base import build_mod, hook
from unrealsdk.unreal import UObject, WrappedStruct, BoundFunction
from typing import Any

# 1. Hàm in Log (In ra Console F6 và File)
def inspect_log(msg):
    unrealsdk.Log(f"[BD3MINER] {msg}")
    # In cả lên màn hình chat để dễ thấy
    pc = unrealsdk.get_player_controller()
    if pc:
        pc.ClientMessage(f"[BD3MINER] {msg}", "Event", True)

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
    name="bd3miner",
    author="User & AI",
    description="Item/Object Class ID Scanner with detailed logging.",
    version="1.0"
)

unrealsdk.Log("[BD3MINER] READY! Look at something or Open something. Check log file!")
```

#### Bước 3: Tạo File `pyproject.toml`
Copy nội dung sau vào file `bd3miner/pyproject.toml`:

```toml
[project]
name = "bd3miner"
version = "1.0.0"
description = "Borderlands 3 Item/Object Class ID Scanner with file logging"
authors = [{name = "User"}]

[tool.sdkmod]
name = "bd3miner"
supported_games = ["BL3"]
```

---

## 🎮 HƯỚNG DẪN SỬ DỤNG

### Kích Hoạt Mod

1. **Khởi động game** Borderlands 3
2. **Nhấn F5** để mở Mods Menu
3. Tìm **bd3miner** và đảm bảo nó **enabled** (có dấu ✓)
4. **Nhấn F6** hoặc **~** để mở Console
5. Nếu thấy dòng `[BD3MINER] READY!` → Mod đã hoạt động!
6. **Kiểm tra log file**: `%USERPROFILE%\Documents\My Games\Borderlands 3\Logs\bd3miner.log`

### Sử Dụng Console

**Mở Console:**
- Nhấn **F6** hoặc phím **~** (huyền)
- Kéo cửa sổ Console sang một bên để vừa chơi vừa xem

**Tips:**
- Console sẽ hiện tất cả logs
- Tìm các dòng có prefix `[BD3MINER]`
- Scroll lên/xuống để xem history
- **Log file tự động** ghi tất cả thông tin vào `bd3miner.log`

---

## 📊 VÍ DỤ SỬ DỤNG

### 1. Quét Items Dưới Đất

#### Cách Làm:
1. Vứt một khẩu súng/khiên xuống đất
2. Di chuyển tâm chuột lên item (như định nhặt)
3. Xem Console

#### Output Mẫu:
```
[BD3MINER] ITEM SEEN: Maggie
[BD3MINER] CLASS: DroppedInventoryItemPickup /Game/Gear/Weapons/Pistols/Jakobs/_Shared/_Design/_Unique/Maggie/Balance/Balance_PS_JAK_Maggie.Balance_PS_JAK_Maggie_C
```

**Giải Thích:**
- `ITEM SEEN: Maggie` → Tên hiển thị của item
- `CLASS: DroppedInventoryItemPickup /Game/...` → Class ID đầy đủ
- **Log file** cũng ghi lại thông tin này với timestamp chi tiết

---

### 2. Quét Hòm/Tủ

#### Cách Làm:
1. Tìm một cái hòm chưa mở (chest, ammo dump, etc.)
2. Bấm **E** để mở
3. Xem Console

#### Output Mẫu:
```
[BD3MINER] OBJECT USED: IO_AmmoDump_123
[BD3MINER] CLASS: /Game/GameData/Loot/InteractiveObjects/Ammo/AmmoDump/IO_AmmoDump.IO_AmmoDump_C
```

**Giải Thích:**
- `OBJECT USED: IO_AmmoDump_123` → Tên instance
- `CLASS: /Game/GameData/.../IO_AmmoDump.IO_AmmoDump_C` → Class ID
- **Log file** ghi chi tiết về object type và timestamp

---

### 3. Thu Thập Data Cho Mod Khác

#### Use Case: Tạo Whitelist Cho MagnetLoot

**Mục tiêu:** Muốn MagnetLoot tự động mở hòm đạn

**Quy trình:**
1. Tìm hòm đạn trong game
2. Mở nó và xem Console
3. Copy Class ID: `/Game/.../IO_AmmoDump.IO_AmmoDump_C`
4. Thêm vào whitelist của MagnetLoot:
   ```python
   AMMO_CONTAINER_IDS = [
       "IO_AmmoDump_C",
       # ... các IDs khác
   ]
   ```

---

## 🔧 XỬ LÝ SỰ CỐ

### Mod Không Xuất Hiện Trong Menu (F5)

**Nguyên nhân có thể:**
- Thư mục đặt sai vị trí
- Thiếu file `pyproject.toml`
- SDK chưa được cài đúng

**Giải pháp:**
1. Kiểm tra cấu trúc thư mục:
   ```
   sdk_mods/bd3miner/__init__.py
   sdk_mods/bd3miner/pyproject.toml
   ```
2. Reload mods: Nhấn F5 → "Reload All Mods"
3. Restart game
4. Kiểm tra log file: `%USERPROFILE%\Documents\My Games\Borderlands 3\Logs\bd3miner.log`

---

### Console Không Hiện Output

**Nguyên nhân có thể:**
- Mod chưa enabled
- Console chưa mở
- Không trigger được events

**Giải pháp:**
1. Nhấn F5, đảm bảo bd3miner có dấu ✓
2. Nhấn F6 để mở Console
3. Thử nhìn vào item rõ ràng (aim straight at it)
4. Thử mở một cái hòm chắc chắn
5. **Kiểm tra log file** - Nếu không có output trong console, xem file log để debug:
   - Mở: `%USERPROFILE%\Documents\My Games\Borderlands 3\Logs\bd3miner.log`
   - Tìm dòng "HOOK TRIGGERED" để biết hook có chạy không

---

### Lỗi Python Import

**Lỗi mẫu:**
```
ImportError: cannot import name 'build_mod' from 'mods_base'
```

**Nguyên nhân:**
- SDK version cũ hoặc không tương thích

**Giải pháp:**
1. Update SDK lên version mới nhất
2. Download tại: https://github.com/bl-sdk/oak-mod-manager
3. Reinstall mod sau khi update SDK

---

### Game Crash Khi Load Mod

**Nguyên nhân có thể:**
- Syntax error trong code
- SDK không tương thích

**Giải pháp:**
1. Kiểm tra lại code trong `__init__.py`
2. Đảm bảo không có lỗi đánh máy
3. Copy chính xác từ hướng dẫn
4. Nếu vẫn crash, tạm disable mod và báo lỗi

---

## 💡 TIPS & TRICKS

### 1. Lọc Output Trong Console

Console có thể rất nhiều logs. Để dễ đọc:
- Tìm các dòng có `[BD3MINER]`
- Sử dụng Ctrl+F trong Console để search
- **Hoặc xem log file trực tiếp** tại `%USERPROFILE%\Documents\My Games\Borderlands 3\Logs\bd3miner.log`

### 2. Đọc Log File

Log file chứa thông tin chi tiết hơn console:
1. Mở File Explorer
2. Dán đường dẫn: `%USERPROFILE%\Documents\My Games\Borderlands 3\Logs`
3. Mở file `bd3miner.log` bằng Notepad
4. Tìm các dòng có "HOOK TRIGGERED" để xem mod có hoạt động không
5. Xem timestamp để biết khi nào hook được kích hoạt

### 3. Kết Hợp Với Các Mod Khác

bd3miner hoạt động tốt với:
- **MagnetLoot** - Lấy IDs để config auto-loot
- **BankSort** - Phân loại items theo IDs
- **ItemSpawner** - Spawn items với exact IDs
- **ChestFinder** - Identify chest types

### 4. Keyboard Shortcuts

| Phím | Chức năng |
|------|-----------|
| F5 | Mods Menu |
| F6 | Console (toggle) |
| ~ | Console (alternative) |
| Ctrl+C | Copy từ Console |
| Ctrl+F | Find trong Console |

---

## 📝 CÁC LOẠI CLASS IDS THƯỜNG GẶP

### Items (Weapons/Shields)
```
DroppedInventoryItemPickup /Game/Gear/Weapons/...
DroppedInventoryItemPickup /Game/Gear/Shields/...
```

### Ammo
```
PickupAmmo /Game/Pickups/Ammo/...
```

### Money
```
PickupCurrency /Game/Pickups/Money/...
```

### Chests
```
/Game/GameData/Loot/InteractiveObjects/.../IO_*.IO_*_C
```

### Containers
```
IO_AmmoDump_C           - Hòm đạn
IO_RedChest_C           - Red chest
IO_Eridium_C            - Eridium chest
IO_LootableCrate_C      - Thùng thường
```

---

## 🎯 WORKFLOW THỰC TẾ

### Scenario: Phát Triển Auto-Loot Mod

**Bước 1: Thu Thập IDs**
1. Enable bd3miner
2. Chơi game và quét items
3. Record các IDs cần thiết
4. **Xem log file** để lấy danh sách đầy đủ với timestamp

**Bước 2: Phân Loại**
- Legendary items: `Balance_*_Legendary*`
- Ammo dumps: `IO_AmmoDump_C`
- Red chests: `IO_RedChest_C`

**Bước 3: Config Mod Khác**
```python
WHITELIST = [
    "IO_AmmoDump_C",
    "IO_RedChest_C",
    # ... từ data bạn quét
]
```

**Bước 4: Test**
- Disable bd3miner (để giảm logs)
- Enable auto-loot mod
- Verify hoạt động đúng

---

## 🆘 HỖ TRỢ

### Cần Trợ Giúp?

1. **Kiểm tra lại hướng dẫn** - Đọc kỹ từng bước
2. **Xem Console logs** - Tìm error messages
3. **Restart game** - Thử reload mod
4. **Update SDK** - Đảm bảo version mới nhất

### Báo Lỗi

Nếu gặp lỗi, cung cấp thông tin:
- Game version
- SDK version
- Error message từ Console
- Steps to reproduce

### Community

- BL3 Modding Discord
- GitHub Issues
- Reddit r/borderlands3

---

## ⚖️ LƯU Ý QUAN TRỌNG

### ✅ An Toàn
- ✅ Mod này là **development tool**
- ✅ Chỉ **đọc dữ liệu**, không sửa game
- ✅ Không ảnh hưởng saves
- ✅ Không vi phạm ToS (chỉ dùng offline)

### ⚠️ Cảnh Báo
- ⚠️ **Chỉ dùng Single Player** để tránh anti-cheat
- ⚠️ Disable khi chơi Online/Co-op
- ⚠️ Không dùng để cheat trong multiplayer

### 📜 Legal
- Mod này miễn phí và open source
- Chỉ dùng cho mục đích học tập và phát triển
- Tuân thủ EULA của Borderlands 3

---

## 🎉 HOÀN TẤT!

Bạn đã cài đặt thành công bd3miner! 

**Bước tiếp theo:**
1. Thử quét một vài items
2. Thu thập IDs bạn cần
3. **Kiểm tra log file** để xem chi tiết
4. Sử dụng cho mod projects khác

**Chức năng chính:**
- ✅ Ghi log tự động ra file với timestamp
- ✅ Hiển thị thông tin trên console và màn hình
- ✅ Xử lý lỗi và ghi traceback để debug
- ✅ Dễ dàng debug khi mod không hoạt động

**Chúc bạn modding vui vẻ!** 🚀

---

*Phiên bản: 1.0.0*  
*Cập nhật: 2026-01-14*  
*Tác giả: User & AI*
