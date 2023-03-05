#!/usr/bin/env python3

from bs4 import BeautifulSoup
import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes


async def bark(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Barks."""
    await update.message.reply_text("Woof!")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Just a help function."""
    help_text = "Available commands:\n"
    help_text += "/bark - Barks.\n"
    help_text += "/concerts - Checks for upcoming classical piano concerts.\n"
    help_text += "/comedy - Checks for upcoming English comedy shows.\n"
    help_text += "/movies - Checks for upcoming movie showings.\n"
    help_text += "/help - Displays this help message.\n"
    await update.message.reply_text(help_text)


async def piano_concerts(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Checks for upcoming classical piano concerts."""
    piano_url = "https://www.tivolivredenburg.nl/agenda/?event_category=piano"
    piano_response = requests.get(piano_url)
    piano_soup = BeautifulSoup(piano_response.content, 'html.parser')

    piano_dates = piano_soup.find_all("time", class_="agenda-list-item__time")
    piano_titles = piano_soup.find_all("a", class_="agenda-list-item__title-link")
    result = ""
    for date, title in zip(piano_dates[:5], piano_titles[5:]):
        result += f"{date.text.strip()} - {title.text.strip()}\n"
    await update.message.reply_text(result)


async def comedy_nights(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Checks for upcoming English comedy shows."""
    comedy_url = "https://comedyhuis.nl/agenda-en-tickets/?_taal=engels"
    comedy_response = requests.get(comedy_url)
    comedy_soup = BeautifulSoup(comedy_response.content, 'html.parser')

    comedy_dates = comedy_soup.find_all("div", class_="fwpl-item el-fum8ad")
    comedy_titles = comedy_soup.find_all("div", class_="fwpl-item el-itawg")
    result = ""
    for date, title in zip(comedy_dates[:5], comedy_titles[5:]):
        result += f"{date.text.strip()} - {title.text.strip()}\n"
    await update.message.reply_text(result)


async def movies(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Checks for upcoming movie showings."""
    movie_url = "https://www.biosagenda.nl/films-bioscoop-bioscopen_utrecht_130.html"
    movie_response = requests.get(movie_url)
    movie_soup = BeautifulSoup(movie_response.content, 'html.parser')

    movie_dates = movie_soup.find_all("th", class_="agenda_th")
    movie_titles = movie_soup.find_all("h3", class_="box_header_title")
    result = ""
    for date, title in zip(movie_dates[:5], movie_titles[5:]):
        result += f"{date.text.strip()} - {title.text.strip()}\n"
    await update.message.reply_text(result)


def main():
    """Starts the bot."""
    # Create the Application
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    application = Application.builder().token(token).build()

    # On different commands - answer in Telegram
    application.add_handler(CommandHandler("bark", bark))
    application.add_handler(CommandHandler("concerts", piano_concerts))
    application.add_handler(CommandHandler("comedy", comedy_nights))
    application.add_handler(CommandHandler("movies", movies))
    application.add_handler(CommandHandler("help", help_command))

    # Run the bot
    application.run_polling()


if __name__ == "__main__":
    main()
