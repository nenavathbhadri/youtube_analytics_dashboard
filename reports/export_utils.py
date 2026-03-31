import pandas as pd
import io


# -----------------------------
# CSV Export
# -----------------------------
def export_csv(df):

    csv_data = df.to_csv(index=False).encode("utf-8")

    return csv_data


# -----------------------------
# Excel Export
# -----------------------------
def export_excel(df):

    df_copy = df.copy()

    # Convert timezone-aware datetimes to timezone-naive
    for col in df_copy.select_dtypes(include=["datetime64[ns, UTC]"]).columns:
        df_copy[col] = df_copy[col].dt.tz_localize(None)

    buffer = io.BytesIO()

    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
        df_copy.to_excel(writer, index=False, sheet_name="Analytics")

    return buffer.getvalue()