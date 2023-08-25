from telegram.ext import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
import instaloader
import os

if not os.path.exists("downloads"):
    os.makedirs("downloads")

updater = Updater("6465496473:AAHhuiiloUHu9i5wSTOujRcfUrGZZ2HLnlc", use_context=True)
bot = updater.bot


def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hello ! Welcome to Rishabh's  bot. Send /help for available commands.")


def help(update: Update, context: CallbackContext):
    update.message.reply_text("""Available Commands:

    /download_insta - Download an Instagram post""")


# def gmail_url(update: Update, context: CallbackContext):
#     update.message.reply_text("Your Gmail link here (I am not giving mine for security reasons)")
#
# def youtube_url(update: Update, context: CallbackContext):
#     update.message.reply_text("YouTube Link => https://www.youtube.com/")
#
# def linkedIn_url(update: Update, context: CallbackContext):
#     update.message.reply_text("LinkedIn URL => https://www.linkedin.com/in/dwaipayan-bandyopadhyay-007a/")
#
# def geeks_url(update: Update, context: CallbackContext):
#     update.message.reply_text("GeeksforGeeks URL => https://www.geeksforgeeks.org/")

def download_insta(update: Update, context: CallbackContext):
    update.message.reply_text("Please send me the Instagram post/reel link.")
    context.user_data['waiting_for_insta_link'] = True


def process_insta_link(update: Update, context: CallbackContext):

        if 'waiting_for_insta_link' in context.user_data and context.user_data['waiting_for_insta_link']:
            insta_link = update.message.text
            try:
                L = instaloader.Instaloader()
                post = instaloader.Post.from_shortcode(L.context, insta_link.split("/")[-2])

                if post.typename == "GraphSidecar":  # For carousel posts
                    media_files = []
                    for sidecar_node in post.get_sidecar_nodes():
                        media_files.append((sidecar_node, sidecar_node.typename))
                else:  # For single media posts
                    media_files = [(post, post.typename)]

                # Send each media file to the user
                for media_item, media_type in media_files:
                    if media_type == "GraphVideo":  # Video content
                        video_url = media_item.video_url
                        if video_url:
                            update.message.reply_video(video=video_url)
                    else:  # Image content
                        image_url = media_item.url
                        update.message.reply_document(document=image_url)

            except Exception as e:
                print("Error:", e)
                update.message.reply_text("Sorry, something went wrong while sending the Instagram post.")
            context.user_data['waiting_for_insta_link'] = False
        else:
            update.message.reply_text("Send /download_insta first to send an Instagram post.")

    # ... (other code remains the same)


# ... (other code remains the same)


def unknown(update: Update, context: CallbackContext):
    update.message.reply_text(f"Sorry, '{update.message.text}' is not a valid command")


updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', help))
#
updater.dispatcher.add_handler(CommandHandler('download_insta', download_insta))
updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, process_insta_link))
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown))

updater.start_polling()
updater.idle()
