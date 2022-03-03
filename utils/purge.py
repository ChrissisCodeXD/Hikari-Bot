



async def purge(channel_id,limit,bot):
    """:cvar
    deletes a amount of given messages in a channel.
    Max amount of messages(limit) is 100 everything about 100 will be ignored.
    """
    messages = bot.rest.fetch_messages(channel_id).limit(limit)
    await bot.rest.delete_messages(channel_id, [msg async for msg in messages])