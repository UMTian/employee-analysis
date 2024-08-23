import streamlit as st
import pandas as pd
import numpy as np
import random
import seaborn as sns
import matplotlib.pyplot as plt
from faker import Faker

# Set a seed for reproducibility
np.random.seed(42)
random.seed(42)

# Generate fictional employee data
fake = Faker()

data = {
    'Employee_ID': [f"E{1000 + i}" for i in range(1, 51)],
    'Name': [fake.name() for _ in range(50)],
    'Department': [random.choice(['IT', 'HR', 'Finance', 'Marketing', 'Engineering', 'Health']) for _ in range(50)],
    'Salary': np.random.randint(20000, 100000, size=50),
    'Years_Experience': np.random.randint(1, 20, size=50),
    'Joining_Date': [fake.date_between(start_date='-5y', end_date='today') for _ in range(50)],
    'Performance_Rating': np.random.choice([1, 2, 3, 4, 5], size=50),
    'Leaves_Taken': np.random.randint(0, 20, size=50),
    'Status': np.random.choice(['Active', 'Inactive'], size=50),
    'Gender': np.random.choice(['Male', 'Female'], size=50)
}

df = pd.DataFrame(data)

# Set the background color to black
st.set_page_config(page_title="Employee Data Dashboard", page_icon=":chart:", layout="wide", initial_sidebar_state="collapsed")

# Streamlit App
st.title("Employee Data Dashboard")

# Create separate selection boxes for each option in the sidebar
option_overview = st.sidebar.checkbox('Overview')
option_salary = st.sidebar.checkbox('Salary')
option_names = st.sidebar.checkbox('Names')
option_comparison = st.sidebar.checkbox('Comparison')

if option_names:
    st.sidebar.header("Filter Data by Department and Date Range")
    # Create a selection box for choosing a department
    selected_department = st.sidebar.selectbox("Select Department", df['Department'].unique())
    # Create a date range slider
    min_date = pd.to_datetime(df['Joining_Date'].min())
    max_date = pd.to_datetime(df['Joining_Date'].max())
    default_start_date = min_date
    default_end_date = max_date
    start_date = st.sidebar.date_input("Select Start Date", min_value=min_date, max_value=max_date,
                                       value=default_start_date)
    end_date = st.sidebar.date_input("Select End Date", min_value=min_date, max_value=max_date, value=default_end_date)

    # Filter the data based on selected department and date range
    filtered_df = df[(df['Department'] == selected_department) & (df['Joining_Date'] >= start_date) & (
            df['Joining_Date'] <= end_date)]

    # Display the filtered data
    st.dataframe(filtered_df)

    # Create a bar chart with the top 10 names based on rank
    st.header("Top 10 Names Based on Rank")

    # Sort the data by rank and select the top 10 names
    top_names_df = filtered_df.sort_values(by='Performance_Rating', ascending=False).head(10)

    # Create a bar chart
    st.bar_chart(top_names_df.set_index('Name')['Performance_Rating'])

    # ------------------------------------------------------------------------------------

    # Find top 10 names with the minimum number of leaves
    top_names_min_leaves = filtered_df.nlargest(10, 'Leaves_Taken').sort_values(by='Leaves_Taken')

    # Create a bar chart with names on the x-axis and leaves on the y-axis
    plt.figure(figsize=(12, 8))
    bar_chart_names_leaves = sns.barplot(x='Name', y='Leaves_Taken', data=top_names_min_leaves, palette='muted')

    # Customize the plot if needed
    plt.title('Top 10 Names with Minimum Leaves')
    plt.xlabel('Names')
    plt.ylabel('Leaves Taken')

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45, ha='right')
    # Display the plot in Streamlit app
    st.pyplot(bar_chart_names_leaves.figure)

    # ------------------------------------------------------------------------------------

    # Create a separate dataframe for the 'Names' option based on the selected experience range
    experience_range_names = st.sidebar.slider("Select Experience Range for Names", min_value=df['Years_Experience'].min(),
                                               max_value=df['Years_Experience'].max(),
                                               value=(df['Years_Experience'].min(), df['Years_Experience'].max()))

    filtered_df_names = df[
        (df['Years_Experience'] >= experience_range_names[0]) & (df['Years_Experience'] <= experience_range_names[1]) &
        (df['Department'] == selected_department) & (df['Joining_Date'] >= start_date) & (df['Joining_Date'] <= end_date)]

    # Create a bar chart with experience on the y-axis and names on the x-axis
    plt.figure(figsize=(12, 8))
    bar_chart_experience_names = sns.barplot(x='Name', y='Years_Experience', data=filtered_df_names,
                                             palette='viridis')

    # Customize the plot if needed
    plt.title('Experience vs Names')
    plt.xlabel('Names')
    plt.ylabel('Years of Experience')
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability

    # Display the plot in Streamlit app
    st.pyplot(bar_chart_experience_names.figure)

# Display content based on the selected options
if option_overview or not any([option_salary, option_names, option_comparison]):
    # Display the generated DataFrame
    st.dataframe(df)

    # Create a scatter plot using Seaborn
    scatter_plot = sns.scatterplot(x='Years_Experience', y='Salary', hue='Gender', style='Department', data=df,
                                   palette='Set1')

    # Add labels and title
    plt.title('Scatter Plot of Experience vs Salary')
    plt.xlabel('Years of Experience')
    plt.ylabel('Salary')

    # Display the legend
    plt.legend(title='Gender')

    # Display the plot in Streamlit app
    st.pyplot(scatter_plot.figure)

    ###########################################################

    # Create a swarm plot with Department on the x-axis and Salary on the y-axis
    swarm_plot_department_salary = sns.swarmplot(x='Department', y='Salary', data=df, hue='Gender', palette='Set1')

    # Customize the plot if needed
    plt.title('Swarm Plot of Department vs Salary')
    plt.xlabel('Department')
    plt.ylabel('Salary')
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability

    # Display the legend
    plt.legend(title='Gender')

    # Display the plot in Streamlit app
    st.pyplot(swarm_plot_department_salary.figure)

if option_salary:
    # Add code for salary-related analysis
    st.header('Salary Analysis')
    # Example: Display a histogram of salaries

    st.caption('Distribution of Salaries')

    st.sidebar.header("Salary Analysis Options")
    salary_analysis_option = st.sidebar.radio("Select Salary Analysis Option",
                                              ["General", "Department", "Experience", "Gender"])

    # Salary analysis based on the selected option
    if salary_analysis_option == "General":
        st.header("General Salary Analysis")
        # Write your analysis code for the general salary analysis here

        # Calculate average salary by department
        avg_salary_by_department = df.groupby('Department')['Salary'].mean().reset_index()

        # Create a bar chart
        st.bar_chart(avg_salary_by_department.set_index('Department')['Salary'])

        # Customize the plot if needed
        plt.title('Average Salary by Department')
        plt.xlabel('Department')
        plt.ylabel('Average Salary')

        # Display the plot in Streamlit app
        st.pyplot(plt.gcf())

    elif salary_analysis_option == "Department":
        st.header("Department-wise Salary Analysis")
        # Write your analysis code for the department-wise salary analysis here
        # Calculate salaries of top 10 employees from each department
        top_10_salaries_by_department = df.groupby('Department').apply(lambda x: x.nlargest(10, 'Salary')).reset_index(
            drop=True)

        # Create separate bar charts for each department
        departments = df['Department'].unique()

        for department in departments:
            st.header(f"Top 10 Salaries - {department}")

            # Filter data for the specific department
            department_data = top_10_salaries_by_department[top_10_salaries_by_department['Department'] == department]

            # Create a bar chart
            st.bar_chart(department_data.set_index('Name')['Salary'])

            # Customize the plot if needed
            plt.title(f'Top 10 Salaries - {department}')
            plt.xlabel('Employee Name')
            plt.ylabel('Salary')

            # Display the plot in Streamlit app
            st.pyplot(plt.gcf())

    elif salary_analysis_option == "Experience":
        st.header("Experience-wise Salary Analysis")
        # Write your analysis code for the experience-wise salary analysis here
        # Create separate bar graphs for each department
        departments = df['Department'].unique()

        for department in departments:
            st.header(f"Salary vs Experience - {department}")

            # Filter data for the specific department
            department_data = df[df['Department'] == department]

            # Create a swarm graph
            swarm_plot = sns.swarmplot(x='Salary', y='Years_Experience', data=department_data, palette='viridis')

            # Customize the plot if needed
            plt.title(f'Salary vs Experience - {department}')
            plt.xlabel('Salary')
            plt.ylabel('Years of Experience')

            # Display the plot in Streamlit app
            st.pyplot(plt.gcf())

    elif salary_analysis_option == "Gender":
        st.sidebar.header("Additional Salary Options")
        # Create buttons for Male and Female analysis
        male_button = st.sidebar.button("Male Analysis")
        female_button = st.sidebar.button("Female Analysis")

        # Male Analysis
        if male_button:
            st.header("Male Analysis")
            # Write your analysis code for Male here
            st.header("Male Analysis by Department")
            # Create a bar chart for each department
            for department in df['Department'].unique():
                male_data = df[(df['Gender'] == 'Male') & (df['Department'] == department)]
                plt.figure(figsize=(10, 6))
                sns.histplot(x='Salary', data=male_data, bins=15, kde=True)
                plt.title(f'Salary Distribution of Males in {department} Department')
                plt.xlabel('Salary')
                plt.ylabel('Frequency')
                st.pyplot(plt.gcf())

        # Female Analysis
        if female_button:
            st.header("Female Analysis")
            # Write your analysis code for Female here
            st.header("Female Analysis by Department")
            # Create a bar chart for each department
            for department in df['Department'].unique():
                female_data = df[(df['Gender'] == 'Female') & (df['Department'] == department)]
                plt.figure(figsize=(10, 6))
                sns.histplot(x='Salary', data=female_data, bins=15, kde=True)
                plt.title(f'Salary Distribution of Males in {department} Department')
                plt.xlabel('Salary')
                plt.ylabel('Frequency')
                st.pyplot(plt.gcf())

if option_comparison:
    # Add code for comparison analysis
    st.header('Comparison Analysis')

    st.sidebar.header("Comparison Options")
    # Create selection buttons for 'Department' and 'Gender'
    comparison_department = st.sidebar.checkbox('Department')
    comparison_gender = st.sidebar.checkbox('Gender')

    comparison_option = st.sidebar.radio("Select Comparison Option", ['Department', 'Gender'])

    if comparison_option == 'Department':
        st.sidebar.header("Department Comparison Options")

        # Average Salary by Department
        st.header("Average Salary by Department")
        avg_salary_department = df.groupby('Department')['Salary'].mean()
        st.bar_chart(avg_salary_department)

        # Average Performance by Department
        st.header("Average Performance by Department")
        avg_performance_department = df.groupby('Department')['Performance_Rating'].mean()
        st.bar_chart(avg_performance_department)

        # Average Experience by Department
        st.header("Average Experience by Department")
        avg_experience_department = df.groupby('Department')['Years_Experience'].mean()
        st.bar_chart(avg_experience_department)

    elif comparison_option == 'Gender':
        st.sidebar.header("Gender Comparison Options")

        # Average Salary by Gender
        st.header("Average Salary by Gender")
        avg_salary_gender = df.groupby('Gender')['Salary'].mean()
        st.bar_chart(avg_salary_gender)

        # Average Performance by Gender
        st.header("Average Performance by Gender")
        avg_performance_gender = df.groupby('Gender')['Performance_Rating'].mean()
        st.bar_chart(avg_performance_gender)

        # Average Experience by Gender
        st.header("Average Experience by Gender")
        avg_experience_gender = df.groupby('Gender')['Years_Experience'].mean()
        st.bar_chart(avg_experience_gender)