import csv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes


# 从 response_codes.csv 读取“Code”与“Message”
def load_qa_from_csv(filepath):
    qa_dict = {}
    with open(filepath, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            keyword = str(row['Code']).strip()
            answer = str(row['Message']).strip()
            qa_dict[keyword] = answer
    return qa_dict

# 加载数据
qa_pairs = load_qa_from_csv("response_codes.csv")
default_reply = "未识别的代码，请确认您输入的是否正确。"

# /start 命令处理
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("您好，请输入错误码或响应码，我将告诉您它的含义。")

# 自动关键词匹配
async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text.strip()
    matched = []

    for keyword, answer in qa_pairs.items():
        if keyword in user_message:
            matched.append(f"[{keyword}] {answer}")

    if matched:
        reply_text = "\n\n".join(matched)
    #else:
    #    reply_text = default_reply

    await update.message.reply_text(reply_text)


def main():
    TOKEN = "8114139207:AAF2bx2_Nab1cNYnOZdbb9SCswC__s3sgbE"  # ← 替换为你自己的 Telegram Token
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_reply))

    print("🤖 Bot 正在运行...")
    app.run_polling()

if __name__ == "__main__":
    main()
