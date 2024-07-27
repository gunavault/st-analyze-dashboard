import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

# Sidebar for master menu
st.sidebar.title("Navigation")
master_menu = st.sidebar.selectbox("Select Master Menu", ["Home", "CPU", "Memory"])

# Submenu for each master menu
if master_menu != "Home":
    submenu = st.sidebar.radio("Select Submenu", ["Kotlin Data", "Flutter Data", "React Native Data", "Comparison"])

# Home tab
if master_menu == "Home":
    st.title("Welcome to the Memory and CPU Usage Dashboard")
    st.write("""
    This dashboard allows you to upload and analyze data for CPU and memory usage across different frameworks:
    - **Kotlin**
    - **Flutter**
    - **React Native**
    
    Use the navigation panel on the left to select the type of data you want to analyze (CPU or Memory), and then choose the specific framework or comparison.
    """)
    st.header("Template CSV Format")
    st.write("""
    Ensure your CSV files follow this format:
    
    - **Interval (sec)**: Time intervals at which data was collected.
    - **Columns for each test/measurement**: Each column represents memory or CPU usage data collected at each interval.

    Example:
    ```csv
    Interval (sec);Test 1;Test 2;Test 3
    0;10;20;30
    1;15;25;35
    2;20;30;40
    ```
    """)

    # Create a CSV template
    csv_template = """Interval (sec);Test 1;Test 2;Test 3
0;10;20;30
1;15;25;35
2;20;30;40"""

    # Provide download button for the template
    st.download_button(
        label="Download CSV Template",
        data=csv_template,
        file_name='template.csv',
        mime='text/csv',
    )

else:
    # File upload widgets for CPU and Memory data
    st.sidebar.title("Upload Files")
    if master_menu == "CPU":
        uploaded_file1 = st.sidebar.file_uploader("Upload Kotlin CSV for CPU", type="csv", key="cpu_kotlin")
        uploaded_file2 = st.sidebar.file_uploader("Upload Flutter CSV for CPU", type="csv", key="cpu_flutter")
        uploaded_file3 = st.sidebar.file_uploader("Upload React Native CSV for CPU", type="csv", key="cpu_reactnative")
    elif master_menu == "Memory":
        uploaded_file1 = st.sidebar.file_uploader("Upload Kotlin CSV for Memory", type="csv", key="memory_kotlin")
        uploaded_file2 = st.sidebar.file_uploader("Upload Flutter CSV for Memory", type="csv", key="memory_flutter")
        uploaded_file3 = st.sidebar.file_uploader("Upload React Native CSV for Memory", type="csv", key="memory_reactnative")

    @st.cache_data
    def load_data(file):
        return pd.read_csv(file, delimiter=';')

    # Load the uploaded files
    if uploaded_file1 is not None:
        data1 = load_data(uploaded_file1)
    if uploaded_file2 is not None:
        data2 = load_data(uploaded_file2)
    if uploaded_file3 is not None:
        data3 = load_data(uploaded_file3)

    # Function to plot data
    def plot_data(data, title):
        plt.figure(figsize=(10, 6))
        for column in data.columns[1:]:
            plt.plot(data['Interval (sec)'], data[column], label=column)
        plt.xlabel('Interval (sec)')
        plt.ylabel('Usage')
        plt.title(title)
        plt.legend()
        st.pyplot(plt)

    # Function to plot comparison data
    def plot_comparison(data1, data2, data3, metric):
        data1['Average'] = data1.iloc[:, 1:].mean(axis=1)
        data2['Average'] = data2.iloc[:, 1:].mean(axis=1)
        data3['Average'] = data3.iloc[:, 1:].mean(axis=1)

        intervals_flutter = data2['Interval (sec)']
        average_flutter = data2['Average']

        intervals_kotlin = data1['Interval (sec)']
        average_kotlin = data1['Average']

        intervals_reactnative = data3['Interval (sec)']
        average_reactnative = data3['Average']

        plt.figure(figsize=(10, 6))
        plt.plot(intervals_flutter, average_flutter, label='Flutter Average Usage', color='red')
        plt.plot(intervals_kotlin, average_kotlin, label='Kotlin Average Usage', color='green')
        plt.plot(intervals_reactnative, average_reactnative, label='React Native Average Usage', color='blue')

        plt.xlabel('Interval (sec)')
        plt.ylabel(f'Average {metric} Usage')
        plt.title(f'Comparison of Average {metric} Usage Across Frameworks')
        plt.legend()
        plt.grid(True)
        st.pyplot(plt)

        # Display average usage
        avg_kotlin = data1['Average'].mean()
        avg_flutter = data2['Average'].mean()
        avg_reactnative = data3['Average'].mean()

        st.subheader(f'Average {metric} Usage')
        st.write(f'Kotlin: {avg_kotlin:.2f}')
        st.write(f'Flutter: {avg_flutter:.2f}')
        st.write(f'React Native: {avg_reactnative:.2f}')

    # Display data and plots based on the selected submenu
    if master_menu == "CPU":
        if submenu == "Kotlin Data" and uploaded_file1 is not None:
            st.title("CPU - Kotlin Data")
            st.write(data1)
            plot_data(data1, 'Kotlin CPU Usage')

        elif submenu == "Flutter Data" and uploaded_file2 is not None:
            st.title("CPU - Flutter Data")
            st.write(data2)
            plot_data(data2, 'Flutter CPU Usage')

        elif submenu == "React Native Data" and uploaded_file3 is not None:
            st.title("CPU - React Native Data")
            st.write(data3)
            plot_data(data3, 'React Native CPU Usage')

        elif submenu == "Comparison" and uploaded_file1 is not None and uploaded_file2 is not None and uploaded_file3 is not None:
            st.title("CPU - Comparison of Average Usage")
            plot_comparison(data1, data2, data3, "CPU")

    elif master_menu == "Memory":
        if submenu == "Kotlin Data" and uploaded_file1 is not None:
            st.title("Memory - Kotlin Data")
            st.write(data1)
            plot_data(data1, 'Kotlin Memory Usage')

        elif submenu == "Flutter Data" and uploaded_file2 is not None:
            st.title("Memory - Flutter Data")
            st.write(data2)
            plot_data(data2, 'Flutter Memory Usage')

        elif submenu == "React Native Data" and uploaded_file3 is not None:
            st.title("Memory - React Native Data")
            st.write(data3)
            plot_data(data3, 'React Native Memory Usage')

        elif submenu == "Comparison" and uploaded_file1 is not None and uploaded_file2 is not None and uploaded_file3 is not None:
            st.title("Memory - Comparison of Average Usage")
            plot_comparison(data1, data2, data3, "Memory")
