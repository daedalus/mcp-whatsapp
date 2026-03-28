# mcp-whatsapp

> MCP server exposing WhatsApp bot functionality with support for multiple adapters.

[![PyPI](https://img.shields.io/pypi/v/mcp-whatsapp.svg)](https://pypi.org/project/mcp-whatsapp/)
[![Python](https://img.shields.io/pypi/pyversions/mcp-whatsapp.svg)](https://pypi.org/project/mcp-whatsapp/)
[![Coverage](https://codecov.io/gh/daedalus/mcp-whatsapp/branch/main/graph/badge.svg)](https://codecov.io/gh/daedalus/mcp-whatsapp)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

## Install

```bash
pip install mcp-whatsapp
```

## WhatsApp Adapters

This package supports two WhatsApp adapters:

- **pywhatkit**: Uses WhatsApp Web (default, easier setup)
- **whatsapp-business**: Uses WhatsApp Business API (production-ready)

### Install with adapter dependencies:

```bash
# For pywhatkit (WhatsApp Web)
pip install mcp-whatsapp[pywhatkit]

# For WhatsApp Business API
pip install mcp-whatsapp[whatsapp-business]
```

## Usage

### Setting the adapter

Set the adapter using the `WHATSAPP_ADAPTER` environment variable:

```bash
export WHATSAPP_ADAPTER=pywhatkit       # Default
export WHATSAPP_ADAPTER=whatsapp-business
```

### WhatsApp Business API Configuration

For WhatsApp Business API, set these environment variables:

```bash
export WHATSAPP_PHONE_NUMBER_ID=your_phone_number_id
export WHATSAPP_ACCESS_TOKEN=your_access_token
export WHATSAPP_VERIFY_TOKEN=your_verify_token
```

### Running as MCP Server

```bash
mcp-whatsapp
```

## MCP Tools

| Tool | Description |
|------|-------------|
| `send_message` | Send a text message to a phone number |
| `send_media` | Send media (image, document) to a phone number |
| `send_location` | Send a location to a phone number |
| `connect_whatsapp` | Connect to the WhatsApp service |
| `disconnect_whatsapp` | Disconnect from the WhatsApp service |

## MCP Resources

| Resource | Description |
|----------|-------------|
| `whatsapp://status` | Get the current connection status |
| `whatsapp://config` | Get the adapter configuration |

## mcp-name

io.github.daedalus/mcp-whatsapp

## Development

```bash
git clone https://github.com/daedalus/mcp-whatsapp.git
cd mcp-whatsapp
pip install -e ".[test]"

# run tests
pytest

# format
ruff format src/ tests/

# lint
ruff check src/ tests/

# type check
mypy src/
```

## License

MIT
