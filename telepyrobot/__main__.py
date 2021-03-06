from pyrogram import Client, __version__
from pyrogram.raw.all import layer

from telepyrobot import API_HASH, APP_ID, LOGGER, STRING_SESSION, load_cmds
from telepyrobot.plugins import ALL_PLUGINS


class TelePyroBot(Client):
    def __init__(self):
        name = self.__class__.__name__.lower()

        super().__init__(
            STRING_SESSION,
            plugins=dict(root=f"{name}/plugins"),
            workdir=f"{name}/session",
            api_id=APP_ID,
            api_hash=API_HASH,
        )

    async def start(self):
        await super().start()
        result = load_cmds(ALL_PLUGINS)
        LOGGER.info(result)

        me = await self.get_me()
        LOGGER.info(
            f"TelePyroBot based on Pyrogram v{__version__} "
            f"(Layer {layer}) started...\n"
            f"Hey {me.first_name}!"
        )

    async def stop(self, *args):
        await super().stop()
        LOGGER.info("TelePyroBot stopped. Bye.")


if __name__ == "__main__":
    TelePyroBot().run()
