import discord
from discord import app_commands
from discord.ext import commands


class Roles(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @app_commands.command()
    @app_commands.checks.has_role('Administrator')
    async def addroles(self, interaction: discord.Interaction):
        """Assign a role to a list of users."""
        assign_role_modal = AssignRoleModal()
        await interaction.response.send_modal(assign_role_modal)

    @addroles.error
    async def addroles_error(interaction: discord.Interaction, error):
        if isinstance(error, discord.app_commands.MissingRole):
            await interaction.response.send_message("You do not have the Administrator role.", ephemeral=True)


def partition_embed(embed: discord.Embed, objList: list[str]) -> discord.Embed:
    startIdx = 0
    endIdx = 0
    fieldIdx = 1
    while endIdx < len(objList):
        charSum = 0
        while charSum <= 1000 and endIdx < len(objList):
            charSum += len(objList[endIdx]) + 1
            endIdx += 1
        if endIdx >= len(objList):
            embed.add_field(name=f"User Page {fieldIdx}", value='\n'.join(
                objList[startIdx:endIdx]))
        else:
            embed.add_field(name=f"User Page {fieldIdx}", value='\n'.join(
                objList[startIdx:endIdx-1]))
            fieldIdx += 1
            startIdx = endIdx - 1
    return embed


class AssignRoleModal(discord.ui.Modal, title="Assign a role to a list of users"):
    role = discord.ui.TextInput(
        style=discord.TextStyle.short,
        label='Role',
        required=True,
        placeholder="Role to be assigned"
    )

    users = discord.ui.TextInput(
        style=discord.TextStyle.long,
        label='User List',
        required=True,
        placeholder="List of users (separated by new lines) to assign the role to"
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()
        successCounter = 0
        role: discord.Role = discord.utils.get(
            interaction.guild.roles, name=self.role.value)
        print(role.name, role.id)
        if not role:
            await interaction.response.send_message(f"Role {self.role.value} not found.", ephemeral=True)
            return
        userList = self.users.value.split('\n')
        confirmList = []
        for username in userList:
            user: discord.Member = discord.utils.find(
                lambda m: m.name == username or m.display_name == username, interaction.guild.members)
            if not user:
                confirmList.append(f":x: {username}")
                print(username)
                continue
            await user.add_roles(role)
            successCounter += 1
            confirmList.append(f":white_check_mark: {username}")
        embed = discord.Embed(
            title=f"{self.role.value} successfully assigned to {successCounter}/{len(userList)} users")
        await interaction.followup.send(embed=partition_embed(embed, confirmList), ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(Roles(bot))
