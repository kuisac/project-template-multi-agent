#!/usr/bin/env python3
"""MCP server — Gemina (Google Gemini bridge) pour l'équipe multi-agents."""

import asyncio
import os
from pathlib import Path

import google.generativeai as genai
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types

TEAM_CHARTER = Path(".claude/shared/team-charter.md")
DEFAULT_MODEL = os.environ.get("GEMINA_MODEL", "gemini-2.5-flash")

SYSTEM_PROMPT = """Tu es Gemina, agent expert externe d'une équipe IA collaborative et adversariale.
Tu es spécialisée dans l'analyse de gros corpus et la synthèse multi-documents (jusqu'à 1M tokens).
Tu n'es pas un assistant généraliste : tu donnes des avis structurés selon une posture précise.
Respecte strictement la posture demandée (Constructeur/Synthétiseur ou Contradicteur) et le format de réponse fourni dans le brief.
Ne sois pas sycophante. Si tu détectes une contradiction, cite les extraits exacts."""

server = Server("gemina")


def _charter() -> str:
    return TEAM_CHARTER.read_text(encoding="utf-8") if TEAM_CHARTER.exists() else ""


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="ask_gemina",
            description=(
                "Soumet un brief à Gemina (Google Gemini) et retourne sa réponse structurée. "
                "Gemina joue la posture Synthétiseur ou Contradicteur selon le brief. "
                "Optimisée pour l'analyse de gros corpus (long context 1M tokens). "
                "La charte de l'équipe est injectée automatiquement en contexte système."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "brief": {
                        "type": "string",
                        "description": (
                            "Le brief complet à soumettre. "
                            "Voir .claude/OtherAI/gemini/brief-template.md pour le format."
                        ),
                    },
                    "model": {
                        "type": "string",
                        "description": f"Modèle Gemini à utiliser. Défaut : {DEFAULT_MODEL}.",
                    },
                },
                "required": ["brief"],
            },
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    if name != "ask_gemina":
        raise ValueError(f"Outil inconnu : {name}")

    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        return [types.TextContent(
            type="text",
            text="ERREUR : variable d'environnement GEMINI_API_KEY non définie. "
                 "Configure-la dans ton environnement Windows ou dans settings.json.",
        )]

    brief = arguments["brief"]
    model_name = arguments.get("model", DEFAULT_MODEL)
    charter = _charter()
    system = SYSTEM_PROMPT
    if charter:
        system += f"\n\n### Charte de l'équipe\n\n{charter}"

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(
        model_name=model_name,
        system_instruction=system,
    )

    loop = asyncio.get_event_loop()
    resp = await loop.run_in_executor(
        None,
        lambda: model.generate_content(brief),
    )

    text = resp.text or ""
    usage = resp.usage_metadata
    footer = (
        f"\n\n---\n"
        f"Agent : Gemina | Modèle : {model_name} | "
        f"Tokens : {usage.prompt_token_count} in / {usage.candidates_token_count} out"
    )
    return [types.TextContent(type="text", text=text + footer)]


async def main() -> None:
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
