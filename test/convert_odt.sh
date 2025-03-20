#!/bin/bash
# 使用 curl 命令將 test/input.odt 檔案傳送到 192.168.100.213
# 20250320-233435

cd $(dirname "$0")

curl -F "file=@input.odt" http://192.168.100.213/
