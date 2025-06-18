from pathlib import Path
from fastmcp import FastMCP
from fastmcp.utilities.types import Image

from src.database import SqliteDatabase
from src.chart import generate_chart


DB_PATH = Path("./data/sensor_readings.db")

mcp = FastMCP(name="Sensor Data Server")


@mcp.tool()
def list_tables():
    """List all available tables in the sensor database"""
    db = SqliteDatabase(DB_PATH)

    results = db.query("SELECT name FROM sqlite_master WHERE type='table'")

    return results


@mcp.tool
def describe_table(table_name: str):
    """Get the schema information for a specific table"""
    db = SqliteDatabase(DB_PATH)

    results = db.get_table_schema(table_name)

    return results


@mcp.tool
def query(sql_query: str):
    """Execute a SELECT query on the sensor database"""
    db = SqliteDatabase(DB_PATH)

    results = db.query(sql_query)

    return results


@mcp.tool
def create_chart(
    columns: list[str],
    rows: list[list],
    chart_type: str = "line",
    x: str | None = None,
    y: str | None = None,
    hue: str | None = None,
    title: str | None = None,
) -> Image:
    """
    Generate a chart from tabular data and return the image file path.

    Example Usage:
    create_chart(
        columns=["date", "region", "revenue"],
        rows=[
            ["2024-01", "SG", 23000],
            ["2024-01", "MY", 18000],
            ["2024-02", "SG", 26000],
            ["2024-02", "MY", 17000]
        ],
        chart_type="line",
        x="date",
        y="revenue",
        hue="region",
        title="Monthly Revenue by Region"
    )

    Parameters:
    - columns: list of column names
    - rows: list of row values
    - chart_type: 'line' or 'bar'
    - x, y: names of columns for x and y axis
    - hue: optional, column name to group lines/bars
    - title: optional chart title

    Returns:
    - Path to saved chart image
    """
    file_path = generate_chart(columns, rows, chart_type, x, y, hue, title)

    # with open(file_path, "rb") as image_file:
    #     encoded_string = base64.b64encode(image_file.read())

    return Image(file_path)


if __name__ == "__main__":
    mcp.run()  # Default: uses STDIO transport
