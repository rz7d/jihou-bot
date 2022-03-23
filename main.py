import discord
import asyncio
import datetime
import io
from zoneinfo import ZoneInfo

JST = ZoneInfo('Asia/Tokyo')

with open(".token", "r") as f:
    token = f.read()

client = discord.Client()

event_loop = asyncio.get_event_loop()


@client.event
async def on_ready():
    print("Ready")
    event_loop.create_task(poll_time())


def canJihou(date: datetime.datetime) -> bool:
    return (date.hour == 0 and date.minute == 0)


async def jihou():
    print("jihou")

    with open(".channels", mode="r", encoding="utf-8") as f:
        channels = f.read()
    print(channels)
    channels = channels.split("\n")

    for channel in channels:
        try:
            channel = int(channel)
        except:
            continue

        channel: discord.VoiceChannel = client.get_channel(channel)
        if not channel:
            continue

        async def play(channel):
            voice_client = await channel.connect()
            source = await discord.FFmpegOpusAudio.from_probe("jihou.opus")

            future = asyncio.Future()

            def leave(exception):
                future.set_result(None)

            voice_client.play(source, after=leave)

            await future
            await voice_client.disconnect()

        event_loop.create_task(play(channel))


async def poll_time():
    lastDate = 0
    while True:
        await asyncio.sleep(0.02)
        now = datetime.datetime.now(JST)
        if lastDate != now.day and canJihou(now):
            lastDate = now.day
            await jihou()
            await asyncio.sleep(60)


async def main():
    print("hello")
    await client.start(token)

event_loop.run_until_complete(main())
