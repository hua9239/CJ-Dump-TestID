# CJ-Dump-TestID

## Requirements 需求
- Python
- pip

## environment 環境
使用前請先安裝 requests 模組，建議使用虛擬環境(venv)。
```bash
pip install requests
```

## Usage 使用方法
於 `main.py` 中，輸入 CloudJudge 的帳號密碼，對應 `email` 和 `password`。

以及當前可用的 課程ID 及 題目ID，對應 `classID` 和 `examID`。

詳細方式可參考 `main.py` 中的註解。

輸入測試範圍 `testRange`，即可執行。

執行中會於當前目錄下產生一個 `result.txt`，內容為測試結果。

若須重新測試，更改 `testRange` 終止值即可接續測試。