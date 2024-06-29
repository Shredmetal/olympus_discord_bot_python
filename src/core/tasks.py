import discord
from discord.ext import tasks
from .shared_state import thread_states

@tasks.loop(hours=24)
async def cleanup_old_threads(bot):
    for guild in bot.guilds:
        for thread in guild.threads:
            if thread.name.startswith("Support for") and (discord.utils.utcnow() - thread.created_at).days > 7:
                try:
                    await thread.delete()
                    thread_states.pop(thread.id, None)
                except discord.HTTPException:
                    pass