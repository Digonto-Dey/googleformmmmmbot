# 📋 Google Form Telegram Bot

A Telegram bot that automates bulk data entry into a Google Form by reading rows from an uploaded Excel file and submitting each row as a form response.

## 🔍 Overview

This project was built to streamline the collection and submission of university student survey data (academic stress, burnout, and well-being) into a Google Form. Instead of manually entering hundreds of rows, users simply send an `.xlsx` file to the Telegram bot and it handles all submissions automatically.

## 🚀 Features

- Accepts `.xlsx` / `.xls` files via Telegram
- Maps Excel column headers to Google Form field IDs using `form_mapping.json`
- Submits each row as a separate Google Form response
- Handles Bengali and English column names
- Reports success/failure counts after processing
- Async processing — bot stays responsive during large uploads

## 🗂️ Project Structure

```
telebot/
├── gformtotelebot.py     # Main bot script
├── form_mapping.json     # Maps Excel column names → Google Form entry IDs
├── requirements.txt      # Python dependencies
├── data.xlsx             # Last uploaded file (auto-generated at runtime)
└── README.md
```

## ⚙️ Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure the bot

Open `gformtotelebot.py` and set:

```python
BOT_TOKEN = "your-telegram-bot-token"
FORM_URL   = "https://docs.google.com/forms/d/e/.../formResponse"
```

### 3. Update field mappings (if the form changes)

Edit `form_mapping.json` to match your Google Form's entry IDs:

```json
{
  "Column Name in Excel": "entry.XXXXXXXXX",
  ...
}
```

To find entry IDs, open your Google Form, inspect the page source, and search for `entry.`.

### 4. Run the bot

```bash
python gformtotelebot.py
```

## 📤 Usage

1. Start a chat with the bot on Telegram and send `/start`
2. Upload your `.xlsx` file containing the survey data
3. The bot will process and submit each row to the Google Form
4. A completion message will confirm how many rows were submitted successfully

## 🛠️ Requirements

| Package | Version |
|---|---|
| python-telegram-bot | ≥ 22.0 |
| pandas | latest |
| openpyxl | latest |
| requests | latest |

## 📝 Notes

- The Excel file's column headers **must exactly match** the keys in `form_mapping.json` (including Bengali characters)
- Rows with no mappable data are skipped automatically
- Empty cells are excluded from form submissions
