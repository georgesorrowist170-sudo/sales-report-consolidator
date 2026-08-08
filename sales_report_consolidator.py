from glob import glob
from pathlib import Path
import pandas as pd


def create_sample_reports(folder_path: Path) -> None:
    """Creates sample monthly sales CSV reports."""
    folder_path.mkdir(parents=True, exist_ok=True)

    (folder_path / "january.csv").write_text(
        "Product,Quantity,Price\n"
        "Milk,20,65\n"
        "Bread,15,80\n"
        "Sugar,40,180"
    )

    (folder_path / "february.csv").write_text(
        "Product,Quantity,Price\n"
        "Milk,30,65\n"
        "Rice,25,210\n"
        "Bread,10,80"
    )

    (folder_path / "march.csv").write_text(
        "Product,Quantity,Price\n"
        "Eggs,60,15\n"
        "Sugar,15,180\n"
        "Sugar,15,180"
    )


def load_reports(folder_path: Path) -> pd.DataFrame:
    """Loads and merges all CSV sales reports."""
    csv_files = glob(str(folder_path / "*.csv"))

    df_list = []

    for file in csv_files:
        df = pd.read_csv(file)
        df_list.append(df)

    merged_df = pd.concat(df_list, ignore_index=True)

    return merged_df


def generate_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Generates a summary DataFrame grouped by Product."""
    totals = df.groupby("Product")["Quantity"].sum()
    average = df.groupby("Product")["Quantity"].mean()
    counts = df.groupby("Product")["Quantity"].count()

    summary_df = pd.DataFrame({
        "Product": totals.index,
        "Total Quantity": totals.values,
        "Average Quantity": average.values,
        "Number of Sales": counts.values
    })

    return summary_df


def print_statistics(df: pd.DataFrame) -> None:
    """Displays overall sales statistics."""
    print(f"Total rows: {len(df)}")
    print(f"Highest quantity: {df['Quantity'].max()}")
    print(f"Lowest quantity: {df['Quantity'].min()}")
    print(f"Average quantity: {df['Quantity'].mean():.2f}")
    print(
        f"Product with highest sale: "
        f"{df.loc[df['Quantity'].idxmax(), 'Product']}"
    )


def save_reports(
    merged_df: pd.DataFrame,
    summary_df: pd.DataFrame
) -> None:
    """Saves the merged sales data and summary report."""
    merged_df.to_csv("merged_sales.csv", index=False)
    summary_df.to_csv("sales_summary.csv", index=False)

    print(
        "Reports successfully saved to "
        "'merged_sales.csv' and 'sales_summary.csv'."
    )


def main() -> None:
    """Runs the sales report consolidation pipeline."""
    reports_dir = Path("Sales_reports")

    create_sample_reports(reports_dir)

    merged_df = load_reports(reports_dir)

    print("--- Merged Sales Data ---")
    print(merged_df)
    print()

    print("--- Overall Statistics ---")
    print_statistics(merged_df)
    print()

    summary_df = generate_summary(merged_df)

    print("--- Product Summary ---")
    print(summary_df)
    print()

    save_reports(merged_df, summary_df)


if __name__ == "__main__":
    main()