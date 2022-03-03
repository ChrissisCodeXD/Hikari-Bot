from FirstBot import FirstBot
import os

if os.name != "nt":
    import uvloop

    uvloop.install()

if __name__ == "__main__":
    bot = FirstBot()
    bot.run()
