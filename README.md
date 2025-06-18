# Sensor DB MCP Server Demo

A minimal **Model Context Protocol (MCP) server** that exposes a synthetic sensor-readings SQLite database and a small chart-generation helper.  
Use it to show how an LLM (e.g. Claude) can *discover* the schema, *query* the data, and *create plots* on demand.


## What’s inside

| Component | Purpose |
|-----------|---------|
| `data/sensor.db` | SQLite DB with two tables:<br>• **sensor** (id, location, type)<br>• **sensor_reading** (sensor_id, timestamp, value) |
| `mcp_server.py` | FastMCP server exposing four tools:<br>• `list_tables()`<br>• `describe_table(table_name)`<br>• `query(sql)` (read-only)<br>• `create_chart(...)` (matplotlib) |


## Quick start

1. Install dependencies  (Python 3.11+ recommended)
```bash
uv pip install fastmcp==2.8.1 matplotlib==3.10.3 pandas==2.3.0
```


### Using with Claude Desktop
Add to your mcp.json (or equivalent):

```jsonc
"sensor_db_server": {
  "command": "uv",
  "args": [
    "--directory",
    "C:\\path\\to\\sensor-db-mcp-server-demo",
    "run",
    "mcp_server.py"
  ]
}
```

## Example Prompts
`How many sensors do we currently have?`

`What's the average temperature in the south zone?`

`Visualize the relationship between temperature and humidity in the north.`