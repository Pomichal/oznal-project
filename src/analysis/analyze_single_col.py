import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class SingleColAnalyser:

    def __init__(self):
        pass

    def analyze_numeric(self, df, column):
        print(df[column].describe())
        print()

        missing = df[column].isna().sum()
        lines = df.shape[0]
        print("missing values: " + str(missing) + "/" + str(lines) + " (" + str(missing / lines) + "%)")

        q1, q3 = df[column].quantile(0.25), df[column].quantile(0.75) 
        iqr = q3 - q1
        lower_bound = q1 -(1.5 * iqr)
        upper_bound = q3 +(1.5 * iqr) 
        out_upper = df[column][df[column] > upper_bound].shape[0]
        out_lower = df[column][df[column] < lower_bound].shape[0]
        print("outliers upper: " + str(out_upper) + "/" + str(lines) + " (" + str(out_upper / lines) + "%)")
        print("outliers lower: " + str(out_lower) + "/" + str(lines) + " (" + str(out_lower / lines) + "%)\n")

        fig, axs = plt.subplots(ncols=2, figsize=(15,5))
        sns.distplot(df[column].dropna(), kde_kws={"color": "b", "lw": 3}, ax=axs[0])
        sns.boxplot(df[column].dropna(), orient='v', ax=axs[1])

        return fig, axs

