import disnake
from disnake import ApplicationCommandInteraction, Option, OptionType
from disnake.ext import commands
from decouple import config

from lunarAPI import Player

bot = commands.Bot(command_prefix="!")
color = 0x8ae8ff


@bot.slash_command(description="This command is used to check to see if the bot is online!")
async def ping(inter: ApplicationCommandInteraction):
    embed = disnake.Embed(title="Pong!", color=color)
    await inter.send(embed=embed, ephemeral=True)


@bot.slash_command(description="This command looks up a player's stats from the Lunar website!",
                   options=[Option("player", description="The player's stats you want to look up!", required=True,
                                   type=OptionType.string)])
async def stats(inter: ApplicationCommandInteraction, player: str):
    p = Player(player)
    if p.isValid():
        name = player
        rank = p.get_rank()
        uuid = p.get_uuid()
        kills = p.get_kills()
        deaths = p.get_deaths()
        kdr = p.get_kdr()
        creds = p.get_credits()
        events = p.get_event_wins()
        high_streak = p.get_highest_streak()
        embed = disnake.Embed(title=f"{name}", url=f"https://www.lunar.gg/u/{name}/souppvp",
                              description=f"****{rank}****",
                              color=color)
        embed.set_thumbnail(url=f"https://crafatar.com/avatars/{uuid}?size=34&overlay")
        embed.add_field(name="Kills", value=f"{kills}", inline=True)
        embed.add_field(name="Deaths", value=f"{deaths}", inline=True)
        embed.add_field(name="KDR", value=f"{kdr}", inline=True)
        embed.add_field(name="Credits", value=f"{creds}", inline=True)
        embed.add_field(name="Events Won", value=f"{events}", inline=True)
        embed.add_field(name="Highest Killstreak", value=f"{high_streak}", inline=True)
        embed.set_footer(text="Lunar Soup - by Otis Goodman")
        await inter.send(embed=embed)
    else:
        embed = disnake.Embed(title="Invalid Player!", color=color)
        await inter.send(embed=embed, ephemeral=True)


bot.run(config("TOKEN"))
