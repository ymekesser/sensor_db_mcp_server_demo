import pandas as pd
import matplotlib.pyplot as plt
import uuid
import os
from datetime import datetime


def generate_chart(
    columns: list[str],
    rows: list[list],
    chart_type: str = "line",
    x: str | None = None,
    y: str | None = None,
    hue: str | None = None,
    title: str | None = None,
) -> str:
    """
    Generate a chart from tabular data and return the image file path.

    Parameters:
    - columns: list of column names
    - rows: list of row values
    - chart_type: 'line', 'bar', or 'scatter'
    - x, y: names of columns for x and y axis
    - hue: optional, column name to group lines/points/bars
    - title: optional chart title

    Returns:
    - Path to saved chart image
    """
    df = pd.DataFrame(rows, columns=columns)
    chart_type = chart_type.lower()

    if x and ("date" in x.lower() or pd.api.types.is_object_dtype(df[x])):
        try:
            df[x] = pd.to_datetime(df[x])
            df = df.sort_values(by=x)
        except Exception:
            pass  # If conversion fails, ignore

    plt.figure(figsize=(10, 6))

    if chart_type == "line":
        if hue:
            for label, group in df.groupby(hue):
                plt.plot(group[x], group[y], label=label)
            plt.legend()
        else:
            plt.plot(df[x], df[y])
    elif chart_type == "bar":
        if hue:
            pivot = df.pivot(index=x, columns=hue, values=y)
            pivot.plot(kind="bar", ax=plt.gca())
        else:
            plt.bar(df[x], df[y])
    elif chart_type == "scatter":
        if hue:
            for label, group in df.groupby(hue):
                plt.scatter(group[x], group[y], label=label)
            plt.legend()
        else:
            plt.scatter(df[x], df[y])
    else:
        raise ValueError(f"Unsupported chart type: {chart_type}")

    plt.title(title or "")
    if x:
        plt.xlabel(x)
    if y:
        plt.ylabel(y)
    plt.xticks(rotation=45)
    plt.tight_layout()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = f"./output/chart_{timestamp}.png"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    plt.savefig(file_path)
    plt.close()

    return file_path
