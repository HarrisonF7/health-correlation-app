"""Run with: uv run --with streamlit,pandas,seaborn,scipy streamlit run app.py"""

from pathlib import Path

import pandas as pd
import seaborn as sns
import streamlit as st
from matplotlib import pyplot as plt


NUMERIC_COLUMNS = [
    "age", "bmi", "waist_cm", "systolic_bp", "diastolic_bp", "hba1c",
    "total_chol", "hdl_chol", "sleep_hours", "sedentary_minutes",
]


@st.cache_data
def load_data(path, modified_time):
    """Cache the CSV while invalidating the cache when the file changes."""
    data = pd.read_csv(path)
    missing = set(NUMERIC_COLUMNS + ["sex"]) - set(data.columns)
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")
    for column in NUMERIC_COLUMNS:
        data[column] = pd.to_numeric(data[column], errors="coerce")
    data[NUMERIC_COLUMNS] = data[NUMERIC_COLUMNS].replace(
        [float("inf"), -float("inf")], float("nan")
    )
    return data


def filter_data(data, sexes, age_range):
    return data.loc[
        data["sex"].isin(sexes)
        & data["age"].between(*age_range, inclusive="both")
    ].copy()


def pair_statistics(data, x, y, method):
    """Use exactly the same complete pairs for the coefficient and count."""
    pairs = data.loc[:, list(dict.fromkeys([x, y]))].dropna(subset=[x, y])
    n = len(pairs)
    if n < 2 or pairs[x].nunique() < 2 or pairs[y].nunique() < 2:
        return pairs, float("nan"), n
    return pairs, pairs[x].corr(pairs[y], method=method), n


def main():
    st.set_page_config(page_title="Health correlations", layout="wide")
    st.title("Health measurement correlations")
    path = Path(__file__).resolve().with_name("nhanes_health.csv")
    try:
        data = load_data(path, path.stat().st_mtime_ns)
    except (OSError, ValueError, pd.errors.ParserError) as error:
        st.error(f"Could not load nhanes_health.csv: {error}")
        st.stop()

    st.sidebar.header("Filters")
    sexes = sorted(data["sex"].dropna().unique().tolist())
    selected_sexes = st.sidebar.multiselect("Sex", sexes, default=sexes)
    ages = data["age"].dropna()
    if ages.empty:
        st.error("The dataset has no valid ages to filter.")
        st.stop()
    minimum, maximum = float(ages.min()), float(ages.max())
    if minimum < maximum:
        age_range = st.sidebar.slider(
            "Age range (inclusive)", minimum, maximum, (minimum, maximum), step=1.0
        )
    else:
        age_range = (minimum, maximum)
        st.sidebar.caption(f"Age: {minimum:g}")
    method = st.sidebar.radio("Correlation method", ["Pearson", "Spearman"]).lower()
    filtered = filter_data(data, selected_sexes, age_range)

    st.write(
        "Explore the health measurements in nhanes_health.csv: age, body size, "
        "blood pressure, HbA1c, cholesterol, sleep, and sedentary time. "
        "Each row is treated as one participant. Sex is categorical and is used "
        "only for filtering. Correlations describe associations, not causation."
    )
    st.metric("Participants after filters", f"{len(filtered):,}")
    st.subheader("Data preview")
    st.dataframe(filtered.head(100), hide_index=True, width="stretch")
    st.caption("First 100 filtered records. All views use the sidebar filters.")
    if filtered.empty:
        st.info("No participants match these filters. Select a sex or expand the age range.")
        st.stop()

    st.subheader("Pairwise correlation")
    left, right = st.columns(2)
    x = left.selectbox("X measurement", NUMERIC_COLUMNS, index=1)
    y = right.selectbox("Y measurement", NUMERIC_COLUMNS, index=2)
    color_threshold = st.checkbox("Color points by systolic blood pressure ≥ 130")
    pairs, r, n = pair_statistics(filtered, x, y, method)
    st.write(f"**{method.title()} r = {r:.3f} · n = {n:,} complete pairs**" if pd.notna(r)
             else f"**{method.title()} r = undefined · n = {n:,} complete pairs**")
    if pd.isna(r):
        st.info("Correlation requires at least two complete pairs and variation in both measurements.")
    if n:
        plot_data = pairs.copy()
        hue = None
        if color_threshold:
            bp = filtered.loc[pairs.index, "systolic_bp"]
            plot_data["BP category"] = bp.map(
                lambda value: "Unknown" if pd.isna(value) else ("≥ 130" if value >= 130 else "< 130")
            )
            hue = "BP category"
        fig, ax = plt.subplots(figsize=(9, 5))
        sns.scatterplot(data=plot_data, x=x, y=y, hue=hue, alpha=0.45, s=25, ax=ax)
        if pairs[x].nunique() > 1:
            bins = pd.cut(pairs[x], bins=min(10, pairs[x].nunique()), duplicates="drop")
            means = pairs.assign(_bin=bins).groupby("_bin", observed=True).agg(
                mean_x=(x, "mean"), mean_y=(y, "mean")
            )
            ax.plot(means.mean_x, means.mean_y, color="black", marker="o", label="Binned means")
        if ax.get_legend_handles_labels()[0]:
            ax.legend()
        ax.set_title(f"{y} versus {x}")
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)
        st.caption("Black line: mean X and Y in up to 10 equal-width X bins, across all displayed points.")
    else:
        st.info("No complete pairs are available for these measurements.")

    st.subheader("Correlation heatmap")
    variables = st.multiselect("Numeric measurements", NUMERIC_COLUMNS, default=NUMERIC_COLUMNS)
    if not variables:
        st.info("Select at least one numeric measurement for the heatmap.")
        return
    correlations = pd.DataFrame(index=variables, columns=variables, dtype=float)
    annotations = pd.DataFrame(index=variables, columns=variables, dtype=str)
    for a in variables:
        for b in variables:
            _, coefficient, count = pair_statistics(filtered, a, b, method)
            correlations.loc[a, b] = coefficient
            label = f"r={coefficient:.2f}" if pd.notna(coefficient) else "r=undefined"
            annotations.loc[a, b] = f"{label}\nn={count:,}"
    fig, ax = plt.subplots(figsize=(max(6, len(variables) * 1.35), max(4, len(variables) * 1.1)))
    # Draw missing correlations in neutral gray, then explicitly annotate every cell.
    ax.set_facecolor("#eeeeee")
    sns.heatmap(
        correlations, vmin=-1, vmax=1, center=0, cmap="vlag",
        linewidths=0.5, linecolor="white", square=True,
        cbar_kws={"label": f"{method.title()} r"}, ax=ax,
    )
    for i, a in enumerate(variables):
        for j, b in enumerate(variables):
            value = correlations.loc[a, b]
            color = "white" if pd.notna(value) and abs(value) > 0.65 else "black"
            ax.text(j + 0.5, i + 0.5, annotations.loc[a, b], ha="center", va="center", color=color, fontsize=8)
    ax.set_title(f"{method.title()} correlations and complete-pair counts")
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
    st.caption("Each cell uses its own complete pairs. Gray cells have undefined r; their n is still shown.")


if __name__ == "__main__":
    main()
