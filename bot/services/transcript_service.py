"""
Transcript Generator Service for support ticket channels.
Generates self-contained, beautifully styled HTML logs of ticket channels.
"""
import html
from datetime import datetime
from typing import List
import discord


class TranscriptService:
    @staticmethod
    async def generate_html(channel: discord.TextChannel, messages: List[discord.Message]) -> str:
        """Generates clean HTML transcript string from Discord messages list."""
        guild_name = html.escape(channel.guild.name if channel.guild else "Server")
        channel_name = html.escape(channel.name)
        generated_at = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

        message_blocks = []
        for msg in messages:
            author_name = html.escape(msg.author.display_name)
            avatar_url = msg.author.display_avatar.url
            timestamp = msg.created_at.strftime("%Y-%m-%d %H:%M:%S")
            content = html.escape(msg.content)
            
            # Format embeds if present
            embed_blocks = ""
            for emb in msg.embeds:
                emb_title = html.escape(emb.title or "")
                emb_desc = html.escape(emb.description or "")
                embed_blocks += f"""
                <div class="embed" style="border-left: 4px solid #{emb.color.value:06x if emb.color else '5865F2'}; padding: 8px 12px; margin-top: 6px; background: rgba(255,255,255,0.05); border-radius: 4px;">
                    {f'<div style="font-weight:bold;">{emb_title}</div>' if emb_title else ''}
                    <div>{emb_desc}</div>
                </div>
                """

            message_blocks.append(f"""
            <div class="message-row" style="display: flex; margin-bottom: 12px;">
                <img src="{avatar_url}" style="width: 40px; height: 40px; border-radius: 50%; margin-right: 12px;">
                <div>
                    <div style="font-size: 0.9em; margin-bottom: 4px;">
                        <span style="font-weight: bold; color: #5865F2;">{author_name}</span>
                        <span style="color: #8E9297; font-size: 0.8em; margin-left: 8px;">{timestamp}</span>
                    </div>
                    <div style="color: #DCDDDE; white-space: pre-wrap;">{content}</div>
                    {embed_blocks}
                </div>
            </div>
            """)

        html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Transcript #{channel_name}</title>
    <style>
        body {{
            background-color: #36393F;
            color: #DCDDDE;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 24px;
        }}
        .header {{
            border-bottom: 1px solid #4F545C;
            padding-bottom: 16px;
            margin-bottom: 24px;
        }}
        .header h1 {{ margin: 0; font-size: 1.5rem; color: #FFFFFF; }}
        .header p {{ margin: 4px 0 0 0; color: #B9BBBE; font-size: 0.9rem; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Ticket Transcript: #{channel_name}</h1>
        <p>Guild: {guild_name} | Total Messages: {len(messages)} | Generated: {generated_at}</p>
    </div>
    <div class="chat-container">
        {"".join(message_blocks)}
    </div>
</body>
</html>
"""
        return html_template


transcript_service = TranscriptService()
