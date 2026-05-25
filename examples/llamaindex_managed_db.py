"""Managed database tools for LlamaIndex agents."""

import hotdata_llamaindex as hli


def main() -> None:
    client = hli.from_env()
    tools = hli.make_hotdata_tools(client)
    by_name = {tool.metadata.name: tool for tool in tools}

    create = by_name["hotdata_create_managed_database"]
    print(
        create.call(
            name="demo_sales",
            schema_name="public",
            tables="orders\ncustomers",
        )
    )

    load = by_name["hotdata_load_managed_table"]
    print(
        load.call(
            database="demo_sales",
            table="orders",
            file="/path/to/orders.parquet",
            schema_name="public",
        )
    )

    client.close()


if __name__ == "__main__":
    main()
