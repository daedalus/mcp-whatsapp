# MCP WhatsApp

MCP server exposing WhatsApp bot functionality.

## When to use this skill

Use this skill when you need to:
- Send messages via WhatsApp
- Send media files
- Send locations

## Tools

- `send_message` - Send text message
- `send_media` - Send image/document
- `send_location` - Send location
- `connect_whatsapp` / `disconnect_whatsapp` - Connection

## Adapters

- pywhatkit (WhatsApp Web)
- whatsapp-business (WhatsApp Business API)

## Install

```bash
pip install mcp-whatsapp[pywhatkit]
# or
pip install mcp-whatsapp[whatsapp-business]
```