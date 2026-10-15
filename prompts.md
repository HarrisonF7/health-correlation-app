## Prompt 1: Initial App Planning

I want to build a Streamlit app called app.py that explores correlations between health measurements in nhanes_health.csv. Please read the CSV before planning. The app should include a short dataset description and data preview, a pairwise correlation view with two dropdowns for X and Y, a scatter plot with a trend line or binned means, the correlation coefficient r and participant count n, and an option to color points using a health threshold such as systolic blood pressure ≥ 130. It should also include a correlation heatmap with selectable numeric variables, sidebar filters for sex and age range, and a toggle between Pearson and Spearman correlations.

The numeric columns are age, bmi, waist_cm, systolic_bp, diastolic_bp, hba1c, total_chol, hdl_chol, sleep_hours, and sedentary_minutes. The sex column is categorical and must never be included in correlation calculations. The sex and age filters must update every view, including the data preview, scatter plot, r, n, and heatmap. Correlations must use only rows with nonmissing values for the relevant variable pair, and n must reflect the number of complete pairs used for each correlation. Show n alongside every r, including heatmap correlations. Fix the heatmap color scale from −1 to 1 regardless of filtering or correlation method.

Use Python, Streamlit, pandas, and seaborn. Keep the app in a single file named app.py, and do not add other packages without asking me first. Do not write code yet. First provide a step-by-step implementation plan explaining the build order, how the filters will feed into every view, the command to run the app, and anything in my request that needs clarification.

## Prompt 2: Update Run Command

The plan looks good! Please update the run command to match my assignment exactly:

`uv run --with streamlit,pandas,seaborn,scipy streamlit run app.py`

Keep everything else the same. Do not write any code yet.


## Prompt 3: Build the Streamlit App

The plan is approved and saved in plan.md. Please begin implementing the Streamlit app in app.py according to the approved plan.

Build the app incrementally, starting with loading the dataset and creating the sidebar filters. Then implement the remaining required features.

Use only the approved packages and make sure the app can run with:

`uv run --with streamlit,pandas,seaborn,scipy streamlit run app.py`

Please explain what you implemented and identify any errors or issues that need my attention.

## Prompt 4: Create Requirements File

Please create a requirements.txt file for my completed Streamlit app, listing the packages needed to deploy app.py. Do not change app.py or any other existing files.