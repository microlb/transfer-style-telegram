import logging
from io import BytesIO
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from model import StyleTransferModel
from TOKEN import TOKEN, REQUEST_KWARGS
#from telegram_transfer_style.test_load_pic import load_and_send_pic
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.

first_image_file = {}


def send_prediction_on_photo(update, context):

    chat_id = update.message.chat_id
    print("Got image from {}".format(chat_id))

    # получаем информацию о картинке
    image_info = update.message.photo[-1]
    image_file = context.bot.get_file(image_info)

    if chat_id in first_image_file:
        # первая картинка, которая к нам пришла станет content image, а вторая style image
        content_image_stream = BytesIO()
        first_image_file[chat_id].download(out=content_image_stream)
        del first_image_file[chat_id]

        style_image_stream = BytesIO()
        image_file.download(out=style_image_stream)
        print(style_image_stream, content_image_stream)
        go = StyleTransferModel()
        output = go.start_learning(content_image_stream, style_image_stream)

        # теперь отправим назад фото
        output_stream = BytesIO()
        output.save(output_stream, format='PNG')
        output_stream.seek(0)
        context.bot.send_photo(chat_id, photo=output_stream)
        print("Sent Photo to user")
    else:
        first_image_file[chat_id] = image_file
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    dp.add_handler(MessageHandler(Filters.photo, send_prediction_on_photo))
    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()