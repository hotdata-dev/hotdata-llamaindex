"""Minimal LlamaIndex tool usage with hotdata-llamaindex."""

import hotdata_llamaindex as hli


def main() -> None:
    client = hli.from_env()
    tools = hli.make_hotdata_tools(client)
    by_name = {tool.metadata.name: tool for tool in tools}

    sql_tool = by_name["hotdata_execute_sql"]
    print(sql_tool.call(sql="SELECT 1 AS ok"))

    list_tool = by_name["hotdata_list_managed_databases"]
    print(list_tool.call())

    client.close()


if __name__ == "__main__":
    main()
