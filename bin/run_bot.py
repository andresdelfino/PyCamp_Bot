import os
from telegram.ext import Application, MessageHandler, filters
from pycamp_bot.commands import auth
from pycamp_bot.commands import voting
from pycamp_bot.commands import manage_pycamp
from pycamp_bot.commands import projects
from pycamp_bot.commands import wizard
from pycamp_bot.commands import base
from pycamp_bot.commands import raffle
from pycamp_bot.commands import schedule
from pycamp_bot.commands import announcements
from pycamp_bot.models import models_db_connection
from pycamp_bot.logger import logger
from pycamp_bot.utils import escape_markdown


async def unknown_command(update, context):
    text = "No reconozco el comando, para ver comandos válidos usá /ayuda"
    await context.bot.send_message(chat_id=update.message.chat_id, text=text)


from pycamp_bot.models import Pycampista
import traceback
async def error_handler(update, context):
    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = "".join(tb_list)
    user = Pycampista.get(Pycampista.username == 'adelfino')
    await context.bot.send_message(
        chat_id=user.chat_id,
        text=repr(context.error) + '\n\n' + tb_string + '\n' + f'User: @{update.message.from_user.username}',
    )


def set_handlers(application):
    base.set_handlers(application)
    auth.set_handlers(application)
    wizard.set_handlers(application)
    voting.set_handlers(application)
    manage_pycamp.set_handlers(application)
    projects.set_handlers(application)
    raffle.set_handlers(application)
    schedule.set_handlers(application)
    announcements.set_handlers(application)
    application.add_handler(MessageHandler(filters.COMMAND, unknown_command))
    application.add_error_handler(error_handler)


if __name__ == '__main__':
    logger.info('Starting PyCamp Bot')

    if 'TOKEN' in os.environ.keys():
        models_db_connection()

        application = Application.builder().token(os.environ['TOKEN']).build()
    # application.add_handler(CommandHandler("start", start))
        set_handlers(application)
        application.run_polling()

    else:
        logger.info('Token not defined. Exiting.')
