import logging
import pandas as pd
import requests
import os
import json
import traceback
import asyncio
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes, CommandHandler

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

BOT_TOKEN = "7883734098:AAE1W8kwmRG10rcECvnBea6UOydh_MqIpjM"
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSe-2fx_ibOrVF-SIuf6tD5mwAHU_-5HKono73i-i1Sy44fEDw/formResponse"

# Load the field mapping
try:
    with open("form_mapping.json", "r", encoding="utf-8") as f:
        MAPPING = json.load(f)
except Exception as e:
    logger.error("Could not load form_mapping.json. Please ensure it exists.")
    MAPPING = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me an Excel (.xlsx) file.")

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    document = update.message.document
    if not document.file_name.endswith(('.xlsx', '.xls')):
        await update.message.reply_text("Please send a valid Excel (.xlsx or .xls) file.")
        return

    status_message = await update.message.reply_text("File received! Processing and sending to Google Form (this may take a few minutes)...")
    
    try:
        file = await document.get_file()
        file_path = "data.xlsx"
        await file.download_to_drive(file_path)

        df = pd.read_excel(file_path)
        df = df.fillna("")

        success = 0
        failed = 0

        for _, row in df.iterrows():
            payload = {}
            for col_name, value in row.items():
                col_str = str(col_name).strip()
                if col_str in MAPPING:
                    entry_id = MAPPING[col_str]
                    # Don't send empty strings if we don't have to
                    val_str = str(value).strip()
                    if val_str:
                        payload[entry_id] = val_str
            
            if not payload:
                continue

            try:
                res = await asyncio.to_thread(requests.post, FORM_URL, data=payload, timeout=10)
                if res.status_code == 200:
                    success += 1
                else:
                    failed += 1
                    logger.warning(f"Failed row: status {res.status_code}. Payload sent: {payload}")
            except Exception as e:
                failed += 1
                logger.error(f"Error submitting row: {e}")

        await status_message.edit_text(f"Done! Submitted {success} rows successfully. Failed {failed} rows. Check terminal for details.")

    except Exception as e:
        logger.error(f"Error processing file: {e}\n{traceback.format_exc()}")
        await status_message.edit_text(f"An error occurred while processing the file:\n{str(e)}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_file))

    app.run_polling()

if __name__ == "__main__":
    main()