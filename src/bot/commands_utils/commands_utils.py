import discord


def has_support_creation_permission(member: discord.Member) -> bool:
    allowed_roles = ["Developer", "Olympian", "Administrator"]  # Add or modify role names as needed
    return any(role.name in allowed_roles for role in member.roles)
