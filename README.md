# BD3Miner - Inspector Tool Mod cho Borderlands 3

## Giới Thiệu

Repository này chứa đánh giá kỹ thuật và implementation cho mod **Inspector Tool** của Borderlands 3. Mod này hoạt động như một "máy quét" để lấy Class IDs chính xác của các items và objects trong game.

## Tài Liệu

- 📄 **[MP Bd3miner](./MP%20Bd3miner)**: Hướng dẫn chi tiết từ tài liệu gốc
- 📊 **[DANH_GIA_KY_THUAT.md](./DANH_GIA_KY_THUAT.md)**: Đánh giá kỹ thuật đầy đủ
- 📖 **[HUONG_DAN_SU_DUNG.md](./HUONG_DAN_SU_DUNG.md)**: Hướng dẫn cài đặt và sử dụng (TIẾNG VIỆT)

## Kết Luận Đánh Giá

### ✅ KẾT LUẬN: MOD NÀY CÓ THỂ LÀM ĐƯỢC

**Độ khả thi**: ⭐⭐⭐⭐⭐ (5/5)

**Lý do chính**:
1. ✅ SDK và API đầy đủ hỗ trợ
2. ✅ Code structure chuẩn mực
3. ✅ Không có rủi ro kỹ thuật
4. ✅ Dễ triển khai và test
5. ✅ Hữu ích cho development

## Chức Năng Chính

Mod Inspector Tool sẽ:

1. **Quét Items**: Khi bạn nhìn vào vật phẩm rơi dưới đất
   - Hiện tên item
   - Hiện Class ID đầy đủ

2. **Quét Objects**: Khi bạn mở hòm/tủ
   - Hiện tên object
   - Hiện Class ID để sử dụng cho mod khác

3. **Hiển thị**: 
   - In ra Console (F6)
   - Hiện trên màn hình chat

## Cấu Trúc Mod

```
InspectorTool/
├── __init__.py        # Code chính của mod (54 dòng)
├── pyproject.toml     # Metadata và cấu hình
└── README.md          # Mô tả ngắn
```

## Yêu Cầu Hệ Thống

- Borderlands 3 (PC)
- BL3 SDK (Unrealsdk + mods_base)
- Python 3.7+

## Tiến Độ

- [x] ✅ Phân tích yêu cầu
- [x] ✅ Đánh giá kỹ thuật
- [x] ✅ Tạo tài liệu đánh giá
- [x] ✅ Xác nhận từ người dùng
- [x] ✅ Triển khai code hoàn tất
- [x] ✅ Tạo hướng dẫn sử dụng tiếng Việt
- [ ] 🧪 Testing bởi người dùng
- [ ] 📦 Release

## Cài Đặt Nhanh

**Cách 1: Từ Repository**
```bash
# Clone repository
git clone https://github.com/nittsdn/bd3miner.git

# Copy thư mục InspectorTool vào sdk_mods/ trong game
```

**Cách 2: Thủ công**
- Copy thư mục `InspectorTool/` vào `<Game>/OakGame/Binaries/Win64/sdk_mods/`
- Xem hướng dẫn chi tiết tại: [HUONG_DAN_SU_DUNG.md](./HUONG_DAN_SU_DUNG.md)

## Liên Hệ

Nếu có câu hỏi hoặc yêu cầu bổ sung, vui lòng tạo issue hoặc comment.

---

**Lưu ý**: Đây là mod development tool, không phải cheat mod. Nó chỉ hiển thị thông tin để hỗ trợ việc phát triển các mod khác.
