# hotdata-llamaindex

LlamaIndex tools for [Hotdata](https://hotdata.dev), built on **hotdata-runtime**.

## Features

- **SQL tool** — run workspace SQL and return JSON rows for agents
- **Managed database tools** — list, create, and load parquet into Hotdata-owned catalogs (replaces legacy dataset uploads)

## Install

```bash
pip install hotdata-llamaindex
```

Requires `HOTDATA_API_KEY`. Optionally set `HOTDATA_WORKSPACE`, `HOTDATA_API_URL`, or `HOTDATA_SANDBOX`.

## Usage

```python
import hotdata_llamaindex as hli

client = hli.from_env()
tools = hli.make_hotdata_tools(client)

for tool in tools:
    print(tool.metadata.name, tool.metadata.description)
```

Managed database example:

```python
tools = {tool.metadata.name: tool for tool in hli.make_hotdata_tools(client)}

tools["hotdata_create_managed_database"].call(
    name="sales",
    schema_name="public",
    tables="orders",
)

tools["hotdata_load_managed_table"].call(
    database="sales",
    table="orders",
    file="/path/to/orders.parquet",
)
```

## Examples

```bash
uv run python examples/llamaindex_basic.py
uv run python examples/llamaindex_managed_db.py
```

## Development

```bash
uv sync --locked
uv run pytest
```
