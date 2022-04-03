async def purge(channel_id, limit, bot, user=None):
    """:cvar
    deletes a amount of given messages in a channel.
    Max amount of messages(limit) is 100 everything about 100 will be ignored.
    """

    messages = bot.rest.fetch_messages(channel_id).limit(limit)

    if user:
        msgs = [msg async for msg in messages if msg.author.id == user.id]
        await bot.rest.delete_messages(channel_id, msgs)
        return len(msgs)
    else:
        msgs = [msg async for msg in messages]
        await bot.rest.delete_messages(channel_id, msgs)
        return len(msgs)
