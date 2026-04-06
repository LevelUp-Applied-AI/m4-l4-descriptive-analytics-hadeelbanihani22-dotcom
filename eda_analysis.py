"""Lab 4 — Descriptive Analytics: Student Performance EDA

Conduct exploratory data analysis on the student performance dataset.
Produce distribution plots, correlation analysis, hypothesis tests,
and a written findings report.

Usage:
    python eda_analysis.py
"""
import os
import pandas as pd
import numpy as np
import matplotlib
from seaborn.objects import KDE
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats



def load_and_profile(filepath):
    """Load the dataset and generate a data profile report.

    Args:
        filepath: path to the CSV file (e.g., 'data/student_performance.csv')

    Returns:
        DataFrame: the loaded dataset

    Side effects:
        Saves a text profile to output/data_profile.txt containing:
        - Shape (rows, columns)
        - Data types for each column
        - Missing value counts per column
        - Descriptive statistics for numeric columns
    """
    # TODO: Load the dataset and report its shape, data types, missing values,
    #       and descriptive statistics to output/data_profile.txt
    
    df= pd.read_csv(filepath)
    with open("output/data_profile.txt", "w") as f:
        f.write(f"Shape: {df.shape}\n\n")
        f.write("Data Types:\n")
        f.write(f"{df.dtypes}\n\n")
        f.write("Missing Values:\n")
        f.write(f"{df.isnull().sum()}\n\n")
        f.write("Descriptive Statistics:\n")
        f.write(f"{df.describe()}\n")       
    return df
def clean_data(df):
    """Clean the dataset by handling missing values and outliers.

    Args:
        df: pandas DataFrame with the student performance data

    Returns:
        pandas DataFrame: the cleaned dataset
    """
    # TODO: Implement data cleaning logic (handle missing values, outliers)
    df=df.copy()

    # Example: Fill missing numeric values with the median
    df['commute_minutes'] = df['commute_minutes'].fillna(df['commute_minutes'].median())
    # Example: Drop rows with missing values in critical columns
    df=df.dropna(subset=['study_hours_weekly'])
    #justification: Missing values in study_hours_weekly (~5%) were dropped due to their small proportion and the importance of this variable, avoiding bias from imputation.
    
    return df


def plot_distributions(df):
    """Create distribution plots for key numeric variables.

    Args:
        df: pandas DataFrame with the student performance data

    Returns:
        None

    Side effects:
        Saves at least 3 distribution plots (histograms with KDE or box plots)
        as PNG files in the output/ directory. Each plot should have a
        descriptive title that states what the distribution reveals.
    
    """
    # TODO: Create distribution plots for numeric columns like GPA,
    #       study hours, attendance, and commute minutes
    # TODO: Use histograms with KDE overlay (sns.histplot) or box plots
    # TODO: Save each plot to the output/ directory
    numeric_cols = ['gpa', 'study_hours_weekly', 'attendance_pct', 'commute_minutes'] #floate columns to plot
    for col in numeric_cols:
        plt.figure(figsize=(8, 6))
        sns.histplot(df[col], kde=True)
        plt.title(f"Distribution of {col} - Reveals central tendency and spread")
        plt.xlabel(col)
        plt.ylabel("Frequency")
        plt.savefig(f"output/{col}_distribution.png")
        plt.close()

        
    plt.figure(figsize=(8, 6))
    sns.boxplot(x='department', y='gpa', data=df)
    plt.title("GPA Distribution Across Departments")
    plt.xlabel("Department")
    plt.ylabel("GPA")
    plt.savefig("output/gpa_by_department_boxplot.png")
    plt.close()
#bar chart for categorical variable example
    plt.figure(figsize=(8, 6))
    sns.countplot(x=df['scholarship'])
    plt.title("Count of Scholarship Status - Reveals distribution of scholarship recipients")
    plt.xlabel("Scholarship Status")
    plt.ylabel("Count")
    plt.savefig("output/scholarship.png")
    plt.close()




def plot_correlations(df):
    """Analyze and visualize relationships between numeric variables.

    Args:
        df: pandas DataFrame with the student performance data

    Returns:
        None

    Side effects:
        Saves at least one correlation visualization to the output/ directory
        (e.g., a heatmap, scatter plot, or pair plot).
    """
    # TODO: Compute the correlation matrix for numeric columns
    # TODO: Create a heatmap or scatter plots showing key relationships
    # TODO: Save the visualization(s) to the output/ directory
    numeric_cols = ['gpa', 'study_hours_weekly', 'attendance_pct', 'commute_minutes']
    corr_matrix = df[numeric_cols].corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
    plt.title("Correlation Matrix of Numeric Variables")
    plt.savefig("output/correlation_heatmap.png")
    plt.close()
    #Create scatter plots for the two most correlated variable pairs (excluding self-correlation)
    corr_pairs = corr_matrix.unstack().sort_values(ascending=False)
    corr_pairs = corr_pairs[corr_pairs < 1]  # Exclude self-correlation-العلاقه مع نفسها
    top_pairs = corr_pairs.head(2).index.tolist()
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x=df[top_pairs[0][0]], y=df[top_pairs[0][1]])
    plt.title(f"Scatter Plot of {top_pairs[0][0]} vs {top_pairs[0][1]} (corr={corr_matrix.loc[top_pairs[0][0], top_pairs[0][1]]:.2f})")
    plt.xlabel(top_pairs[0][0])
    plt.ylabel(top_pairs[0][1])
    plt.savefig(f"output/scatter_{top_pairs[0][0]}vs{top_pairs[0][1]}.png")
    plt.close()





def run_hypothesis_tests(df):
    """Run statistical tests to validate observed patterns.

    Args:
        df: pandas DataFrame with the student performance data

    Returns:
        dict: test results with keys like 'internship_ttest', 'dept_anova',
              each containing the test statistic and p-value

    Side effects:
        Prints test results to stdout with interpretation.

    Tests to consider:
        - t-test: Does GPA differ between students with and without internships?
        - ANOVA: Does GPA differ across departments?
        - Correlation test: Is the correlation between study hours and GPA significant?
    """
    # TODO: Run at least two hypothesis tests on patterns you observe in the data
    # TODO: Report the test statistic, p-value, and your interpretation
    results = {}

    # تقسيم البيانات
    internship_gpa = df[df['has_internship'] == 'Yes']['gpa']
    no_internship_gpa = df[df['has_internship'] == 'No']['gpa']

    # T-test
    t_stat, p_val = stats.ttest_ind(internship_gpa, no_internship_gpa, equal_var=False, nan_policy='omit')

    # Cohen's d
    mean_diff = internship_gpa.mean() - no_internship_gpa.mean()
    pooled_std = np.sqrt(
        ((internship_gpa.std() ** 2 + no_internship_gpa.std() ** 2) / 2)
    )
    cohens_d = mean_diff / pooled_std

    # حفظ النتائج
    results['internship_ttest'] = {
        't_statistic': t_stat,
        'p_value': p_val,
        'cohens_d': cohens_d
    }

    # الطباعة
    print("Hypothesis 1: “Students with internships have higher GPAs than those without internships.”")
    print("\nInternship vs GPA T-test\n -------------------------")
    print(f"T-statistic: {t_stat:.4f}\n")
    print(f"P-value: {p_val:.4f}\n")
    print(f"Cohen's d: {cohens_d:.4f}\n")
    print("Explanation of the results:")
    # التفسير (Plain language)
    if p_val < 0.05:
        print("Interpretation: Students with internships have a statistically higher GPA than those without internships.")
    else:
        print("Interpretation: There is no statistically significant difference in GPA between students with and without internships.")

    
    #ANOVA test for GPA across departments
    print("\nHypothesis 2: “GPA differs across departments.”")  
    dept_groups = [group['gpa'].dropna() for name, group in df.groupby('department')]
    f_stat, p_val = stats.f_oneway(*dept_groups)    
    results['dept_anova'] = {
        'f_statistic': f_stat,
        'p_value': p_val
    }
    print("\nGPA Across Departments ANOVA Test\n --------------------------------")
    print(f"F-statistic: {f_stat:.4f}\n")
    print(f"P-value: {p_val:.4f}\n")    

#Hypothesis 2: “Scholarship status is associated with department.”
#Use a chi-square test: pd.crosstab() then scipy.stats.chi2_contingency()
#Report: chi-square statistic, p-value, degrees of freedom, and a plain-language interpretation
#Print all test results to the console and include them in your findings report.
    print("\nHypothesis 2: “Scholarship status is associated with department.”")
    scholarship_dept_table = pd.crosstab(df['scholarship'], df['department'])
    chi2_stat, p_val, dof, expected = stats.chi2_contingency(scholarship_dept_table)
    results['scholarship_dept_chi2'] = {    
        'chi2_statistic': chi2_stat,
        'p_value': p_val,
        'degrees_of_freedom': dof
    }           
    print("\nScholarship Status vs Department Chi-Square Test\n ---------------------------------------------")
    print(f"Chi-square statistic: {chi2_stat:.4f}\n")   
    print(f"P-value: {p_val:.4f}\n")
    print(f"Degrees of freedom: {dof}\n")   
    return results


def main():
    """Orchestrate the full EDA pipeline."""
    os.makedirs("output", exist_ok=True)

    # TODO: Load and profile the datasetplot
    # TODO: Generate distribution plots
    # TODO: Analyze correlations
    # TODO: Run hypothesis tests
    # TODO: Write a FINDINGS.md summarizing your analysis
    df=load_and_profile("data/student_performance.csv")   
    df=clean_data(df)
    plot_distributions(df)
    plot_correlations(df)
    run_hypothesis_tests(df)



if __name__ == "__main__":
    main()
