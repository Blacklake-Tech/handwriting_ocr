# 手写单据识别 handwriting_ocr

[![CI](https://github.com/Blacklake-Tech/handwriting_ocr/actions/workflows/ci.yml/badge.svg)](https://github.com/Blacklake-Tech/handwriting_ocr/actions/workflows/ci.yml)

基于[百度云API][baidu]和[讯飞云API][xf]的手写单据识别 demo app，同时使用了 streamlit 构建 UI 界面。

Handwriting OCR using [Baidu cloud API][baidu] and [Xfyun API][xf].

## Running locally

Setup poetry (one time setup):

```bash
python -m pip install -U pip
python -m pip install poetry
```

Write your environment files:

```bash
# for xfyun, please generate your XF_APP_ID and XF_APP_KEY from https://www.xfyun.cn/doc/platform/quickguide.html
# for baidu, please generate your credentials from https://console.bce.baidu.com/ai/#/ai/ocr/app/list
# and put them here
echo > .env <<EOF
# 如果你用的是讯飞云 API
XF_APP_ID=<app_id>
XF_APP_KEY=<app_key>
# 如果你用的是百度 API，注意区分 APP/API
BAIDU_APP_ID=<app_id>
BAIDU_API_KEY=<app_key>
BAIDU_API_SECRET=<app_secret>
EOF
```

Running via `poetry`:

```bash
# install dependencies
poetry install --no-root
# run the app
poetry run streamlit run handwriting_ocr/app.py
```

## Developing

If you have updated the dependencies, please run:

```bash
poetry lock
```

### Formatting code using `black` and `isort`

```bash
poetry run isort . --profile black
poetry run black .
```

[baidu]: https://cloud.baidu.com/doc/OCR/s/Al1zvpylt
[xf]: https://www.xfyun.cn/doc/words/wordRecg/API.html
