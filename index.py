import asyncio
import traceback

from config import SUPER_DRUG_BASE_URLS
from fetcher import fetch_all_pages
from logger import Logger
from discord import send_welcome_message_to_discord
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime


async def startBot():
    # Log current time before starting the bot
    current_time = datetime.now().isoformat()
    Logger.warn(f"Current time before starting the bot: {current_time}")

    for index, url in enumerate(SUPER_DRUG_BASE_URLS):
        try:
            # Send a welcome message to Discord channel
            await send_welcome_message_to_discord(url)

            # Fetch data from Superdrug API
            Logger.warn(f"Fetching data from Superdrug API {index + 1} of {len(SUPER_DRUG_BASE_URLS)}", url)
            await fetch_all_pages(url)
        except Exception as error:
            traceback.print_exc()
            Logger.error(f"Error fetching data from Superdrug API {index + 1} of {len(SUPER_DRUG_BASE_URLS)} - {url}",
                         error)
        finally:
            Logger.info(f"Finished fetching data from Superdrug API {index + 1} of {len(SUPER_DRUG_BASE_URLS)}", url)

    Logger.debug('Sleeping till next cron job')


if __name__ == "__main__":
    scheduler = AsyncIOScheduler()

    # Add cron jobs
    # scheduler.add_job(startBot, 'cron', minute='*/2', timezone='GMT')
    scheduler.add_job(startBot, 'cron', hour='1', timezone='GMT')
    scheduler.add_job(startBot, 'cron', hour='9', timezone='GMT')
    scheduler.add_job(startBot, 'cron', hour='16', timezone='GMT')

    # Run startBot immediately when the script starts
    scheduler.add_job(startBot)

    # Start the scheduler
    scheduler.start()

    # Keep the event loop running
    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass
