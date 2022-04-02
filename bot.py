import disnake
from disnake import ApplicationCommandInteraction, Option, OptionType
from disnake.app_commands import Choices, OptionChoice
from disnake.ext import commands
from decouple import config

from lunarAPI import Player, Leaderboard, LeaderboardNameHelper

bot = commands.Bot()
color = 0x8ae8ff
NameHelper = LeaderboardNameHelper()


@bot.slash_command(description="This command is used to check to see if the bot is online!")
async def ping(inter: ApplicationCommandInteraction):
    embed = disnake.Embed(title="Pong!", color=color)
    await inter.send(embed=embed, ephemeral=True)


@bot.slash_command(description="This command looks up a player's stats from the Lunar website!",
                   options=[Option("player", description="The player's stats you want to look up!", required=True,
                                   type=OptionType.string)])
async def stats(inter: ApplicationCommandInteraction, player: str):
    p = Player(player)
    if p.is_valid():
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


@bot.slash_command(description="This command looks up the current leaderboard!",
                   options=[
                       Option("category", "The category of the leaderboard!", type=OptionType.string, required=True,
                              choices=NameHelper.create_options()),
                       Option("page", "The page of the leaderboard!", type=OptionType.integer, required=False,
                              min_value=1)
                   ])
async def leaderboard(inter: ApplicationCommandInteraction, category: str, page: int = 1):
    lb = Leaderboard(page, category)
    if lb.is_valid():
        url = lb.url
        players = lb.get_players()
        ranks = lb.get_ranks()
        stats = lb.get_stats()
        embed = disnake.Embed(title=f"🏆 Leaderboard", url=lb.url,
                              color=color)
        i = 0
        ret = []
        while i <= 19:
            ret.append(f"{ranks[i]}: **{players[i]}** `{stats[i]}`\n")
            i = i + 1
        if page != 1:
            ret.append(f"(*page: {page}*)")
        embed.add_field(f"{NameHelper.get_real_name(category)}:", str().join(ret), inline=False)
        embed.set_footer(text="Lunar Soup - by Otis Goodman")
        await inter.send(embed=embed)
    else:
        embed = disnake.Embed(title="Invalid Page!", color=color)
        await inter.send(embed=embed, ephemeral=True)


bot.run(config("TOKEN"))
