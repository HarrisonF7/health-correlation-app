
## Correlation Verification

| # | Check | App shows | pandas gives | Match? |
|---|---|---|---|---|
| 1 | r for age vs systolic_bp, all participants | r = 0.46 | r = 0.462695 | Yes |
| 2 | r for bmi vs waist_cm, all participants | r = 0.90 | r = 0.902589 | Yes |
| 3 | r for waist_cm vs hdl_chol, all participants | r = -0.33 | r = -0.334987 | Yes |
| 4 | r and n for age vs systolic_bp, Female only | r = 0.555, n = 2,263 | r = 0.555343, n = 2,263 | Yes |
| 5 | r and n for age vs systolic_bp, Male only | r = 0.351, n = 2,170 | r = 0.350698, n = 2,170 | Yes |
| 6 | Female-only heatmap: age vs systolic_bp | r = 0.56, n = 2,263 | r = 0.555343, n = 2,263 | Yes |


## M9 Trap

A correlation coefficient close to zero does not necessarily mean there is no relationship between two variables. Pearson correlation measures linear relationships, so a non-linear relationship, such as a U-shaped pattern between sleep hours and a health measurement, may have a correlation close to zero.

The heatmap also needs a fixed color scale from -1 to 1 so that the colors accurately represent the strength and direction of correlations.

## Code Check

I reviewed the Streamlit app code to make sure that the calculations use the filtered dataset. The sex and age filters are applied before calculating correlations, and the categorical sex column is excluded from the correlation calculations.

The app removes missing values separately for each pair of measurements, so the correlation coefficient and participant count use the same observations. The Pearson/Spearman selection applies to both the scatter plot results and the heatmap. The heatmap uses a fixed color scale from -1 to 1.

I also independently verified six correlation results using pandas, and all six matched the app's displayed results within rounding differences.