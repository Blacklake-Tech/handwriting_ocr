# 手写单据识别 handwriting_ocr

[![CI](https://github.com/Blacklake-Tech/handwriting_ocr/actions/workflows/ci.yml/badge.svg)](https://github.com/Blacklake-Tech/handwriting_ocr/actions/workflows/ci.yml)

Handwriting OCR using [Xfyun API](https://www.xfyun.cn/doc/words/wordRecg/API.html).

## Running locally

Setup poetry (one time setup):

```bash
python -m pip install -U pip
python -m pip install poetry
```

Write your environment files:

```bash
# please generate your APP_ID and APP_KEY from https://www.xfyun.cn/doc/platform/quickguide.html
# and put it here
echo > .env <<EOF
APP_ID=<app_id>
APP_KEY=<app_key>
EOF
```

Running via poetry:

```bash
poetry run streamlit run handwriting_ocr/src/handwriting_ocr.py
```

## Formatting code using black

```bash
poetry run black .
```
