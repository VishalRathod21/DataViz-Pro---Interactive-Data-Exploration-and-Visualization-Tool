import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go

# Set page configuration
st.set_page_config(
    page_title='Consoleflare Analytics Portal',
    page_icon='📊',
)

# Title
st.title(":red[Data] Master")

# Subheader with description of the purpose of the app
st.subheader("Effortless :red[Exploration, Transformation, and Visualization]", divider="rainbow")
st.write(":grey[The objective of this Data Master web application is to provide users with an intuitive and interactive platform for performing comprehensive data analysis tasks. This app is designed to assist data analysts, data scientists, and business professionals in quickly understanding and exploring datasets, transforming data as needed, and generating meaningful insights through various data visualization techniques.]")

# File upload description and instructions
st.subheader("Upload Your Dataset", divider="rainbow")
st.write(":grey[To begin your analysis, simply upload a CSV, Excel, or JSON file containing the dataset you want to explore. This platform will assist you with multiple functionalities including data preview, cleaning, transformation, and visualization.]")

# File uploader widget
file = st.file_uploader("Drop csv or excel or json file", type=['csv', 'xlsx', 'json'])

# File size validation and loading
if file:
    if file.size > 10 * 1024 * 1024:  # 10 MB limit
        st.warning("File size is too large. Please upload a file less than 10MB.")
    else:
        try:
            if file.name.endswith('csv'):
                data = pd.read_csv(file, encoding='ISO-8859-1')  # You can also try 'latin1' or 'utf-16'
            elif file.name.endswith('xlsx'):
                data = pd.read_excel(file)
            elif file.name.endswith('json'):
                data = pd.read_json(file)
            
            # Displaying the dataframe
            st.dataframe(data)
            st.info('File is successfully uploaded', icon='🚨')

            # Data Summary Tabs
            st.subheader(':rainbow[Basic Information of the Dataset]', divider='rainbow')
            tab1, tab2, tab3, tab4 = st.tabs(['Summary', 'Top and Bottom Rows', 'Data Types', 'Columns'])

            with tab1:
                st.write(f'There are {data.shape[0]} rows and {data.shape[1]} columns in the dataset.')
                st.subheader(':gray[Statistical Summary of the Dataset]')
                st.dataframe(data.describe())

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

            # Basic Data Operations - Value Count
            st.subheader(':rainbow[Column Values to Count]', divider='rainbow')
            with st.expander('Value Count'):
                col1, col2 = st.columns(2)
                with col1:
                    column = st.selectbox('Choose Column Name', options=list(data.columns))
                with col2:
                    toprows = st.number_input('Top rows', min_value=1, step=1)
                
                count = st.button('Count')
                if count:
                    result = data[column].value_counts().reset_index().head(toprows)
                    st.dataframe(result)
                    st.subheader('Visualizations', divider='gray')

                    # Bar chart
                    fig = px.bar(data_frame=result, x=column, y='count', text='Count')
                    st.plotly_chart(fig)

                    # Line chart
                    fig = px.line(data_frame=result, x=column, y='count', text='Count')
                    st.plotly_chart(fig)

                    # Pie chart
                    fig = px.pie(data_frame=result, names=column, values='count')
                    st.plotly_chart(fig)

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
                    graph_type = st.selectbox("Choose graph type", options=["line", "bar", "scatter", "pie", "sunburst", "histogram"])

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

            # Export Data
            st.subheader(':rainbow[Export Processed Data]', divider='rainbow')
            export_option = st.radio('Choose export format', ['CSV', 'Excel'])
            if export_option == 'CSV':
                st.download_button(label="Download CSV", data=data_cleaned.to_csv(), file_name="cleaned_data.csv", mime="text/csv")
            elif export_option == 'Excel':
                st.download_button(label="Download Excel", data=data_cleaned.to_excel(), file_name="cleaned_data.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

        except Exception as e:
            st.error(f"Error loading the file: {e}")
