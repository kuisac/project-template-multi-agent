#!/usr/bin/env python3
"""MCP server — Gepetto (OpenAI/GPT bridge) pour l'équipe multi-agents."""

import asyncio
import os
from pathlib import Path

from openai import AsyncOpenAI
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types

TEAM_CHARTER = Path(".claude/shared/team-charter.md")
DEFAULT_MODEL = os.environ.get("GEPETTO_MODEL", "gpt-4.1")

SYSTEM_PROMPT = """Tu es Gepetto, agent expert externe d'une équipe IA collaborative et adversariale.
Tu n'es pas un assistant généraliste : tu donnes des avis structurés selon une posture précise.
Respecte strictement la posture demandée (Constructeur ou Contradicteur) et le format de réponse fourni dans le brief.
Ne sois pas sycophante. Si tu n'es pas convaincu, dis-le clairement."""

server = Server("gepetto")


def _charter() -> str:
    return TEAM_CHARTER.read_text(encoding="utf-8") if TEAM_CHARTER.exists() else ""


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="ask_gepetto",
            description=(
                "Soumet un brief à Gepetto (OpenAI GPT) et retourne sa réponse structurée. "
                "Gepetto joue la posture Constructeur ou Contradicteur selon le brief. "
                "La charte de l'équipe est injectée automatiquement en contexte système."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "brief": {
                        "type": "string",
                        "description": (
                            "Le brief complet à soumettre. "
                            "Voir .claude/OtherAI/gpt/brief-template.md pour le format."
                        ),
                    },
                    "model": {
                        "type": "string",
                        "description": f"Modèle OpenAI à utiliser. Défaut : {DEFAULT_MODEL}.",
                    },
                },
                "required": ["brief"],
            },
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    if name != "ask_gepetto":
        raise ValueError(f"Outil inconnu : {name}")

    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        return [types.TextContent(
            type="text",
            text="ERREUR : variable d'environnement OPENAI_API_KEY non définie. "
                 "Configure-la dans ton environnement Windows ou dans settings.json.",
        )]

    brief = arguments["brief"]
    model = arguments.get("model", DEFAULT_MODEL)
    charter = _charter()
    system = SYSTEM_PROMPT
    if charter:
        system += f"\n\n### Charte de l'équipe\n\n{charter}"

    client = AsyncOpenAI(api_key=api_key)
    resp = await client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": brief},
        ],
        temperature=0.7,
    )

    text = resp.choices[0].message.content or ""
    u = resp.usage
    footer = (
        f"\n\n---\n"
        f"Agent : Gepetto | Modèle : {model} | "
        f"Tokens : {u.prompt_tokens} in / {u.completion_tokens} out"
    )
    return [types.TextContent(type="text", text=text + footer)]


async def main() -> None:
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
