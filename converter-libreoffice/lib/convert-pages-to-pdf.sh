#!/bin/bash

# 輸入檔案：MAC pages的檔案路徑
# 將檔案解壓縮，取得裡面的pdf
# 複製到跟輸入檔案同樣的路徑下，取同樣的檔名，但副檔名是pdf
# 20250321-121715

# 取得輸入檔案的路徑
INPUT_FILE="$1" # 20250321-121715

# 檢查輸入檔案是否存在
if [ ! -f "$INPUT_FILE" ]; then # 20250321-121715
  echo "檔案不存在: $INPUT_FILE" # 20250321-121715
  exit 1 # 20250321-121715
fi # 20250321-121715

# 建立暫存資料夾，用來存放解壓縮的檔案
TEMP_DIR=$(mktemp -d) # 20250321-121715

# 解壓縮pages檔案
unzip "$INPUT_FILE" -d "$TEMP_DIR" # 20250321-121715

# 尋找解壓縮後的pdf檔案
PDF_FILE=$(find "$TEMP_DIR" -name "Preview.pdf") # 20250321-121715

# 檢查pdf檔案是否存在
if [ ! -f "$PDF_FILE" ]; then # 20250321-121715
  echo "找不到 PDF 檔案" # 20250321-121715
  rm -rf "$TEMP_DIR" # 20250321-121715
  exit 1 # 20250321-121715
fi # 20250321-121715

# 取得輸出檔案的路徑
OUTPUT_FILE="${INPUT_FILE%.*}".pdf # 20250321-121715

# 複製pdf檔案到輸出路徑
cp "$PDF_FILE" "$OUTPUT_FILE" # 20250321-121715

# 移除暫存資料夾
rm -rf "$TEMP_DIR" # 20250321-121715

echo "轉換完成: $OUTPUT_FILE" # 20250321-121715

exit 0 # 20250321-121715
