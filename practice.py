import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the data from the saved file
df = pd.read_excel('dataset.xlsx')  # Load from Excel file

# Convert 'Joining_Date' to datetime if it's not already
df['Joining_Date'] = pd.to_datetime(df['Joining_Date'])

# Set the background color to black
st.set_page_config(page_title="Employee Data Dashboard", page_icon=":chart:", layout="wide",
                   initial_sidebar_state="collapsed")

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
    min_date = df['Joining_Date'].min()
    max_date = df['Joining_Date'].max()
    start_date = st.sidebar.date_input("Select Start Date", min_value=min_date, max_value=max_date, value=min_date)
    end_date = st.sidebar.date_input("Select End Date", min_value=min_date, max_value=max_date, value=max_date)

    # Filter the data based on selected department and date range
    filtered_df = df[(df['Department'] == selected_department) & (df['Joining_Date'] >= pd.to_datetime(start_date)) & (
                df['Joining_Date'] <= pd.to_datetime(end_date))]

    # Display the filtered data
    st.dataframe(filtered_df)

    # Create a bar chart with the top 10 names based on rank
    st.header("Top 10 Names Based on Rank")
    top_names_df = filtered_df.sort_values(by='Performance_Rating', ascending=False).head(10)
    st.bar_chart(top_names_df.set_index('Name')['Performance_Rating'])

    # Find top 10 names with the minimum number of leaves
    top_names_min_leaves = filtered_df.nsmallest(10, 'Leaves_Taken')
    plt.figure(figsize=(12, 8))
    sns.barplot(x='Name', y='Leaves_Taken', data=top_names_min_leaves, palette='muted')
    plt.title('Top 10 Names with Minimum Leaves')
    plt.xlabel('Names')
    plt.ylabel('Leaves Taken')
    plt.xticks(rotation=45, ha='right')
    st.pyplot(plt.gcf())
    plt.close()

    # Create a separate dataframe for the 'Names' option based on the selected experience range
    experience_range_names = st.sidebar.slider("Select Experience Range for Names",
                                               min_value=int(df['Years_Experience'].min()),
                                               max_value=int(df['Years_Experience'].max()), value=(
        int(df['Years_Experience'].min()), int(df['Years_Experience'].max())))
    filtered_df_names = filtered_df[(filtered_df['Years_Experience'] >= experience_range_names[0]) & (
                filtered_df['Years_Experience'] <= experience_range_names[1])]

    # Create a bar chart with experience on the y-axis and names on the x-axis
    plt.figure(figsize=(12, 8))
    sns.barplot(x='Name', y='Years_Experience', data=filtered_df_names, palette='viridis')
    plt.title('Experience vs Names')
    plt.xlabel('Names')
    plt.ylabel('Years of Experience')
    plt.xticks(rotation=45)
    st.pyplot(plt.gcf())
    plt.close()

if option_overview or not any([option_salary, option_names, option_comparison]):
    st.dataframe(df)

    scatter_plot = sns.scatterplot(x='Years_Experience', y='Salary', hue='Gender', style='Department', data=df,
                                   palette='Set1')
    plt.title('Scatter Plot of Experience vs Salary')
    plt.xlabel('Years of Experience')
    plt.ylabel('Salary')
    plt.legend(title='Gender')
    st.pyplot(plt.gcf())
    plt.close()

    swarm_plot_department_salary = sns.swarmplot(x='Department', y='Salary', data=df, hue='Gender', palette='Set1')
    plt.title('Swarm Plot of Department vs Salary')
    plt.xlabel('Department')
    plt.ylabel('Salary')
    plt.xticks(rotation=45)
    plt.legend(title='Gender')
    st.pyplot(plt.gcf())
    plt.close()

if option_salary:
    st.header('Salary Analysis')
    st.caption('Distribution of Salaries')

    st.sidebar.header("Salary Analysis Options")
    salary_analysis_option = st.sidebar.radio("Select Salary Analysis Option",
                                              ["General", "Department", "Experience", "Gender"])

    if salary_analysis_option == "General":
        st.header("General Salary Analysis")
        avg_salary_by_department = df.groupby('Department')['Salary'].mean().reset_index()
        st.bar_chart(avg_salary_by_department.set_index('Department')['Salary'])
        plt.title('Average Salary by Department')
        plt.xlabel('Department')
        plt.ylabel('Average Salary')
        st.pyplot(plt.gcf())
        plt.close()

    elif salary_analysis_option == "Department":
        st.header("Department-wise Salary Analysis")
        top_10_salaries_by_department = df.groupby('Department').apply(lambda x: x.nlargest(10, 'Salary')).reset_index(
            drop=True)
        for department in df['Department'].unique():
            st.header(f"Top 10 Salaries - {department}")
            department_data = top_10_salaries_by_department[top_10_salaries_by_department['Department'] == department]
            st.bar_chart(department_data.set_index('Name')['Salary'])
            plt.title(f'Top 10 Salaries - {department}')
            plt.xlabel('Employee Name')
            plt.ylabel('Salary')
            st.pyplot(plt.gcf())
            plt.close()

    elif salary_analysis_option == "Experience":
        st.header("Experience-wise Salary Analysis")
        for department in df['Department'].unique():
            st.header(f"Salary vs Experience - {department}")
            department_data = df[df['Department'] == department]
            sns.swarmplot(x='Salary', y='Years_Experience', data=department_data, palette='viridis')
            plt.title(f'Salary vs Experience - {department}')
            plt.xlabel('Salary')
            plt.ylabel('Years of Experience')
            st.pyplot(plt.gcf())
            plt.close()

    elif salary_analysis_option == "Gender":
        st.sidebar.header("Additional Salary Options")
        male_button = st.sidebar.button("Male Analysis")
        female_button = st.sidebar.button("Female Analysis")

        if male_button:
            st.header("Male Analysis")
            for department in df['Department'].unique():
                male_data = df[(df['Gender'] == 'Male') & (df['Department'] == department)]
                plt.figure(figsize=(10, 6))
                sns.histplot(x='Salary', data=male_data, bins=15, kde=True)
                plt.title(f'Salary Distribution of Males in {department} Department')
                plt.xlabel('Salary')
                plt.ylabel('Frequency')
                st.pyplot(plt.gcf())
                plt.close()

        if female_button:
            st.header("Female Analysis")
            for department in df['Department'].unique():
                female_data = df[(df['Gender'] == 'Female') & (df['Department'] == department)]
                plt.figure(figsize=(10, 6))
                sns.histplot(x='Salary', data=female_data, bins=15, kde=True)
                plt.title(f'Salary Distribution of Females in {department} Department')
                plt.xlabel('Salary')
                plt.ylabel('Frequency')
                st.pyplot(plt.gcf())
                plt.close()

if option_comparison:
    st.header('Comparison Analysis')

    st.sidebar.header("Comparison Options")
    comparison_option = st.sidebar.radio("Select Comparison Option", ['Department', 'Gender'])

    if comparison_option == 'Department':
        st.sidebar.header("Department Comparison Options")

        st.header("Average Salary by Department")
        avg_salary_department = df.groupby('Department')['Salary'].mean()
        st.bar_chart(avg_salary_department)

        st.header("Average Performance by Department")
        avg_performance_department = df.groupby('Department')['Performance_Rating'].mean()
        st.bar_chart(avg_performance_department)

        st.header("Average Experience by Department")
        avg_experience_department = df.groupby('Department')['Years_Experience'].mean()
        st.bar_chart(avg_experience_department)

    elif comparison_option == 'Gender':
        st.sidebar.header("Gender Comparison Options")

        st.header("Average Salary by Gender")
        avg_salary_gender = df.groupby('Gender')['Salary'].mean()
        st.bar_chart(avg_salary_gender)

        st.header("Average Performance by Gender")
        avg_performance_gender = df.groupby('Gender')['Performance_Rating'].mean()
        st.bar_chart(avg_performance_gender)

        st.header("Average Experience by Gender")
        avg_experience_gender = df.groupby('Gender')['Years_Experience'].mean()
        st.bar_chart(avg_experience_gender)

