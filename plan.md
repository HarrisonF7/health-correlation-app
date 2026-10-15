I read `nhanes_health.csv`. It contains **4,433 rows**, the ten numeric columns you listed, and categorical `sex` values of Female (2,263) and Male (2,170). Ages range from **20 to 80**, and no missing values were found. The app will still handle missing values correctly.

1. **Load and validate the data.** Create a single `app.py` that loads the CSV relative to the app’s location. Define an explicit allowlist of the ten numeric variables so `sex` can never enter correlation calculations. Show a clear error for missing files or required columns.

2. **Build the sidebar controls.** Add a sex multiselect, an inclusive age-range slider defaulting to 20–80, and a Pearson/Spearman selector. Default to both sexes and the full age range.

3. **Create one shared filtered dataset.** Apply sex and age filters immediately after loading. Every subsequent view will use this dataset: the displayed participant count, data preview, scatter plot, pairwise statistics, and heatmap. Streamlit will recompute these views whenever a control changes.

4. **Add the description and preview.** Briefly describe the available health measurements, display the filtered row count, and show a preview of filtered records. Avoid claiming a specific NHANES survey cycle or sampling methodology without supporting metadata.

5. **Implement pairwise statistics.** Provide X and Y dropdowns containing only the numeric allowlist. For the chosen pair, remove rows missing either measurement, then calculate the selected correlation method and **n from those same complete pairs**. Show undefined correlations clearly when there are fewer than two pairs or either variable is constant.

6. **Build the scatter plot and threshold coloring.** Use seaborn to plot the complete pairs with binned means overlaid. Add an optional color toggle for systolic blood pressure **≥ 130**, with a clear legend. Coloring will not change the rows used for r or n; missing blood-pressure values, if introduced later, will receive an “Unknown” category.

7. **Build the correlation heatmap.** Add a multiselect for numeric variables. Calculate each cell independently using rows complete for that specific pair, and annotate every cell with both values, such as `r = 0.42` and `n = 583`. Keep the color scale fixed at **−1 to 1**, centered at zero, for both methods and all filters. Undefined cells will still display their n.

8. **Verify behavior.** Check that sex and age changes update every view; pairwise statistics agree with the corresponding heatmap cell; missing values produce pair-specific counts; and empty selections, constant variables, and small subsets render useful messages.

Run the completed app from the project directory with:

```bash
uv run --with streamlit,pandas,seaborn,scipy streamlit run app.py
```

**Clarifications and proposed defaults:** Nothing blocks implementation. I propose binned means, which you explicitly allow, and a fixed optional threshold of systolic BP ≥ 130. Seaborn uses Matplotlib for rendering; I would use that existing dependency without adding or installing another package. The dataset description will remain general unless you provide its survey cycle, provenance, and measurement units.

No code or files have been changed.