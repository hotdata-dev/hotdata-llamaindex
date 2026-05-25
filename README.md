# hotdata-llamaindex

Give your [LlamaIndex](https://www.llamaindex.ai/) agents access to [Hotdata](https://hotdata.dev) — run SQL against your workspace connections and work with managed databases.

## Install

```bash
pip install hotdata-llamaindex
```

## Authentication

Set `HOTDATA_API_KEY` in your environment. Optionally set `HOTDATA_WORKSPACE` to pin a specific workspace (the first available workspace is used if unset).

## Quickstart

```python
from llama_index.core.agent.workflow import FunctionAgent
import hotdata_llamaindex as hli

client = hli.from_env()
tools = hli.make_hotdata_tools(client)

agent = FunctionAgent(tools=tools, llm=your_llm)
response = await agent.run("How many rows are in the orders table?")
```

## Tools

`make_hotdata_tools(client)` returns a list of LlamaIndex `FunctionTool` objects ready to pass to any agent:

| Tool | What it does |
|------|-------------|
| `hotdata_execute_sql` | Run a SQL query and return rows as JSON |
| `hotdata_list_managed_databases` | List available managed databases |
| `hotdata_create_managed_database` | Create a new managed database |
| `hotdata_load_managed_table` | Load a parquet file into a managed table |

## Calling tools directly

You can also call tools outside of an agent loop:

```python
tools = {t.metadata.name: t for t in hli.make_hotdata_tools(client)}

result = tools["hotdata_execute_sql"].call(sql="SELECT * FROM orders LIMIT 10")
print(result.content)  # JSON rows

tools["hotdata_create_managed_database"].call(
    name="sales",
    schema_name="public",
    tables="orders,customers",
)

tools["hotdata_load_managed_table"].call(
    database="sales",
    table="orders",
    file="/path/to/orders.parquet",
)
```

## Scoping queries to a managed database

Pass `database=` so all SQL the agent runs resolves against a specific managed database:

```python
tools = hli.make_hotdata_tools(client, database="sales")
```

## Controlling result size

Limit how many rows are returned to the LLM. Useful for keeping responses within context limits (default: 100):

```python
tools = hli.make_hotdata_tools(client, max_rows=50)
```

## Run the examples

```bash
uv run python examples/llamaindex_basic.py
uv run python examples/llamaindex_managed_db.py
```

## Development

```bash
uv sync --locked
uv run pytest
```
