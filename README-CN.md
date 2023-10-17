<p align="center">
  <a href="./README.md">English</a> |
  <a href="./README-CN.md">繁體中文</a>
</p>

# 浮水印應用說明

這套腳本允許你在指定目錄的圖片上添加浮水印。提供了兩種不同的方法：

1. `filled_watermark.py` - 對`target.csv`中指定的圖片添加浮水印。
2. `rectangle_watermark.py` - 對符合特定檔名模式的圖片添加浮水印。

## 設定

1. 安裝 Python (建議使用3.6或更高版本)。
2. 使用pip安裝所需的庫：
   ```bash
   pip install Pillow tqdm
   ```

## 使用方式

### `filled_watermark.py`

此腳本將浮水印添加到`target.csv`中指定的圖片上。

**使用方法**:
```bash
python filled_watermark.py [浮水印路徑] [目標文件夾] [輸出文件夾]
```

**參數**:
- `浮水印路徑`: 浮水印圖片的路徑。
- `目標文件夾`: 包含要添加浮水印的圖片的目錄。
- `輸出文件夾`: 保存加了浮水印圖片的目錄。

在使用此腳本前，請在同一目錄下創建一個`target.csv`，格式如下：
```
file_name,status
image1.jpg,no
image2.jpg,yes
...
```

設為"no"的圖片將被處理。

腳本將在`輸出文件夾`生成一個`output_status.csv`，指出每個圖片的處理狀態。

### `rectangle_watermark.py`

此腳本將浮水印添加到符合特定檔名模式的圖片上：`^P\d{13}_(1|2|3|4)_.*\.(jpeg|jpg|png|JPG)$`。

**使用方法**:
```bash
python rectangle_watermark.py [浮水印路徑] [目標文件夾] [輸出文件夾]
```

**參數**:
- `浮水印路徑`: 浮水印圖片的路徑。
- `目標文件夾`: 包含要添加浮水印的圖片的目錄。
- `輸出文件夾`: 保存加了浮水印圖片的目錄。

腳本將在浮水印圖片的同一目錄下生成一個`output_status.csv`，指出每個圖片的處理狀態。

## 注意事項

- 這兩個腳本將處理圖片，並在添加浮水印之前通過添加白色填充使其成為正方形。
- 如果在處理過程中發生任何錯誤，它們將在`output_status.csv`文件中被記錄。

## 貢獻

如果你發現任何錯誤或有建議，請開啟一個問題或提交拉取請求。歡迎貢獻！

## 授權

此項目使用MIT授權。詳情請參見[LICENSE](LICENSE)文件。