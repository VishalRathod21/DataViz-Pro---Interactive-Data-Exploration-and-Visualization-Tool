import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st

# Assuming 'data' is your DataFrame
# Data Summary Tabs
st.subheader(':rainbow[Basic Information of the Dataset]', divider='rainbow')
tab1, tab2, tab3, tab4 = st.tabs(['Summary', 'Top and Bottom Rows', 'Data Types', 'Columns'])

with tab1:
    st.write(f'There are {data.shape[0]} rows and {data.shape[1]} columns in the dataset.')
    st.subheader(':gray[Statistical Summary of the Dataset]')
    st.dataframe(data.describe())

    # Descriptive statistics summary
    st.subheader(":blue[Descriptive Statistics Summary]")
    st.write("Mean, Standard Deviation, Min, Max, 25th, 50th, 75th Percentile for each numeric column:")
    st.dataframe(data.describe())

    # Missing Values Summary
    st.subheader(":blue[Missing Values Summary]")
    missing_values = data.isnull().sum()
    missing_percentage = (missing_values / data.shape[0]) * 100
    missing_data = pd.DataFrame({"Missing Values": missing_values, "Percentage": missing_percentage})
    st.dataframe(missing_data)

    # Correlation Matrix Heatmap
    st.subheader(":blue[Correlation Matrix]")
    if data.select_dtypes(include=['number']).shape[1] > 1:  # Only if there's more than one numeric column
        corr = data.corr()
        fig = plt.figure(figsize=(8, 6))
        sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f', cbar=True)
        st.pyplot(fig)
    else:
        st.write("Not enough numeric columns to generate a correlation matrix.")

with tab2:
    st.subheader(':gray[Top Rows]')
    toprows = st.slider('Number of rows to display', 1, data.shape[0], key='topslider')
    st.dataframe(data.head(toprows))
    st.subheader(':gray[Bottom Rows]')
    bottomrows = st.slider('Number of rows to display', 1, data.shape[0], key='bottomslider')
    st.dataframe(data.tail(bottomrows))

with tab3:
    st.subheader(':gray[Data Types of Columns]')
    st.dataframe(data.dtypes)

with tab4:
    st.subheader('Column Names in Dataset')
    st.write(list(data.columns))

# Advanced Groupby Operations
st.subheader(':rainbow[Groupby: Simplify Your Data Analysis]', divider='rainbow')
st.write('The groupby method lets you summarize data by specific categories and groups.')

with st.expander('Group By your columns'):
    col1, col2, col3 = st.columns(3)
    with col1:
        groupby_cols = st.multiselect('Choose columns to group by', options=list(data.columns))
    with col2:
        operation_col = st.selectbox('Choose column for operation', options=list(data.columns))
    with col3:
        operation = st.selectbox('Choose operation', options=['sum', 'max', 'min', 'mean', 'count'])
    
    if groupby_cols:
        result = data.groupby(groupby_cols).agg(
            newcol=(operation_col, operation)
        ).reset_index()

        st.dataframe(result)

        # Data Visualization
        st.subheader(":red[Data Visualization]", divider="rainbow")
        graph_type = st.selectbox("Choose graph type", options=["line", "bar", "scatter", "pie", "sunburst", "histogram", "boxplot"])

        if graph_type == "line":
            x_axis = st.selectbox("Choose X axis", options=list(result.columns))
            y_axis = st.selectbox("Choose Y axis", options=list(result.columns))
            color = st.selectbox("Choose color info", options=[None] + list(result.columns))
            fig = px.line(data_frame=result, x=x_axis, y=y_axis, color=color, markers="o")
            st.plotly_chart(fig)

        elif graph_type == "bar":
            x_axis = st.selectbox("Choose X axis", options=list(result.columns))
            y_axis = st.selectbox("Choose Y axis", options=list(result.columns))
            color = st.selectbox("Choose color info", options=[None] + list(result.columns))
            facet_col = st.selectbox("Choose column info", options=[None] + list(result.columns))
            fig = px.bar(data_frame=result, x=x_axis, y=y_axis, color=color, facet_col=facet_col, barmode="group")
            st.plotly_chart(fig)

        elif graph_type == "scatter":
            x_axis = st.selectbox("Choose X axis", options=list(result.columns))
            y_axis = st.selectbox("Choose Y axis", options=list(result.columns))
            color = st.selectbox("Choose color info", options=[None] + list(result.columns))
            size = st.selectbox("Choose size", options=[None] + list(result.columns))
            fig = px.scatter(data_frame=result, x=x_axis, y=y_axis, color=color, size=size)
            st.plotly_chart(fig)

        elif graph_type == "pie":
            names = st.selectbox("Choose labels", options=list(result.columns))
            values = st.selectbox("Choose numerical values", options=list(result.columns))
            fig = px.pie(data_frame=result, names=names, values=values)
            st.plotly_chart(fig)

        elif graph_type == "sunburst":
            path = st.multiselect("Choose path", options=list(result.columns))
            fig = px.sunburst(data_frame=result, path=path, values="newcol")
            st.plotly_chart(fig)

        elif graph_type == "histogram":
            column = st.selectbox("Choose Column for Histogram", options=list(result.columns))
            fig = px.histogram(data_frame=result, x=column)
            st.plotly_chart(fig)

        elif graph_type == "boxplot":
            column = st.selectbox("Choose Column for Boxplot", options=list(result.columns))
            fig = px.box(data_frame=result, y=column)
            st.plotly_chart(fig)

# Data Cleaning Options (Optional)
st.subheader(':rainbow[Data Cleaning]', divider='rainbow')
with st.expander('Clean the Data'):
    if st.checkbox('Remove Duplicates'):
        data_cleaned = data.drop_duplicates()
        st.dataframe(data_cleaned)

    if st.checkbox('Handle Missing Values'):
        missing_strategy = st.selectbox('Choose strategy', options=['Drop', 'Fill'])
        if missing_strategy == 'Drop':
            data_cleaned = data.dropna()
        else:
            fill_value = st.text_input('Fill with value', '')
            data_cleaned = data.fillna(fill_value)
        st.dataframe(data_cleaned)

    if st.checkbox('Rename Columns'):
        column_rename = {col: st.text_input(f"New name for {col}", col) for col in data.columns}
        data_cleaned = data.rename(columns=column_rename)
        st.dataframe(data_cleaned)

# Export Data without using BytesIO
st.subheader(':rainbow[Export Processed Data]', divider='rainbow')
export_option = st.radio('Choose export format', ['CSV', 'Excel'])

if export_option == 'CSV':
    # Directly export CSV without using BytesIO
    st.download_button(
        label="Download CSV",
        data=data_cleaned.to_csv(index=False),
        file_name="cleaned_data.csv",
        mime="text/csv"
    )
elif export_option == 'Excel':
    # Directly export Excel without using BytesIO
    st.download_button(
        label="Download Excel",
        data=data_cleaned.to_excel(index=False),
        file_name="cleaned_data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
