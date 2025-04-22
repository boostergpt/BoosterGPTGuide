import streamlit as st
import pandas as pd
import numpy as np

# Set page configuration
st.set_page_config(
    page_title="Vibe Coding Guide",
    page_icon="🌈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .highlight {
        background-color: #f6f6f6;
        border-radius: 5px;
        padding: 15px;
        border-left: 3px solid #4e8cff;
    }
    .command-box {
        background-color: #1e1e1e;
        color: white;
        border-radius: 5px;
        padding: 10px;
        font-family: monospace;
    }
    h1, h2, h3, h4 {
        margin-top: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Define a function to display code blocks
def display_code_block(text):
    st.markdown(f"""
    <div class="highlight">
        <pre>{text}</pre>
    </div>
    """, unsafe_allow_html=True)

# Define the initial dashboard code
initial_dashboard_code = '''import pandas as pd
import numpy as np
import streamlit as st
import altair as alt
from datetime import datetime
import plotly.express as px
import re

def load_data():
    """
    Load CSV data using Streamlit's file uploader.
    Returns:
        pandas.DataFrame: The loaded data or None if no file is uploaded.
    """
    st.sidebar.header("Upload Data")
    
    uploaded_file = st.sidebar.file_uploader(
        "Choose a CSV file",
        type="csv",
        help="Upload your auto dealership data in CSV format"
    )
    
    if uploaded_file is not None:
        try:
            data = pd.read_csv(uploaded_file)            
            st.sidebar.success(f"Successfully loaded data with {data.shape[0]} rows and {data.shape[1]} columns")
            return data
        except Exception as e:
            st.sidebar.error(f"Error loading data: {e}")
            return None
    else:
        st.sidebar.info("Please upload a CSV file to begin analysis")
        return None

def file_explorer(data):
    """
    Display the raw data table with options to sort and filter.
    
    Args:
        data (pandas.DataFrame): The dataframe to display
    """
    if data is not None:
        st.header("Data Explorer")
        
        with st.expander("Show Raw Data", expanded=False):
            # Display dataframe with column configuration
            st.dataframe(
                data,
                use_container_width=True,
                height=400
            )

def filter_values(data):
    """
    Provide filtering capabilities for the dataframe.
    
    Args:
        data (pandas.DataFrame): The dataframe to filter
        
    Returns:
        pandas.DataFrame: The filtered dataframe
    """
    if data is None:
        return None
    
    st.header("Data Filtering")
    
    filtered_data = data.copy()
    
    with st.expander("Filter Data", expanded=True):
        # Create columns for filter layout
        cols = st.columns(3)
        
        # Process each column in the dataframe
        filter_count = 0
        for i, column in enumerate(data.columns):
            # Determine column type
            is_numeric = pd.api.types.is_numeric_dtype(data[column])
            is_datetime = pd.api.types.is_datetime64_dtype(data[column])
            is_categorical = (not is_numeric and not is_datetime) or (is_numeric and data[column].nunique() < 20)
            
            # Place in appropriate column (cycling through the 3 columns)
            with cols[filter_count % 3]:
                if is_categorical:
                    # For categorical data or numeric with few unique values
                    # Handle mixed types by converting to strings before sorting
                    unique_values = data[column].unique()
                    try:
                        unique_values = sorted(unique_values)
                    except TypeError:
                        # If sorting fails due to mixed types, convert to strings
                        unique_values = sorted(unique_values.astype(str))
                    
                    selected_values = st.multiselect(
                        f"Select {column}",
                        options=unique_values,
                        default=[]
                    )
                    
                    if selected_values:
                        filtered_data = filtered_data[filtered_data[column].isin(selected_values)]
                        
                elif is_datetime:
                    # For datetime columns
                    min_date = data[column].min().date()
                    max_date = data[column].max().date()
                    
                    date_range = st.date_input(
                        f"Filter {column}",
                        value=(min_date, max_date),
                        min_value=min_date,
                        max_value=max_date
                    )
                    
                    if len(date_range) == 2:
                        start_date, end_date = date_range
                        filtered_data = filtered_data[
                            (filtered_data[column].dt.date >= start_date) & 
                            (filtered_data[column].dt.date <= end_date)
                        ]
                        
                else:
                    # For continuous numeric data
                    min_val = float(data[column].min())
                    max_val = float(data[column].max())
                    
                    value_range = st.slider(
                        f"Filter {column}",
                        min_value=min_val,
                        max_value=max_val,
                        value=(min_val, max_val),
                        step=(max_val - min_val) / 100
                    )
                    
                    filtered_data = filtered_data[
                        (filtered_data[column] >= value_range[0]) & 
                        (filtered_data[column] <= value_range[1])
                    ]
                
                filter_count += 1
    
    # Show filtering stats
    if len(filtered_data) < len(data):
        st.info(f"Filtered data: {len(filtered_data)} rows (from {len(data)} total)")
    
    return filtered_data

def main():
    """
    Main application function that orchestrates the dashboard.
    """
    try:
        # Set page config
        st.set_page_config(
            page_title="Analytics Dashboard",
            page_icon="🚗",
            layout="wide"
        )
        
        # Add title and description
        st.title("Analytics Dashboard")
        st.markdown("""
        This is your starting point for any analytical project.
        """)
        
        # Load data
        data = load_data()
        
        if data is not None:
            # Filter data
            filtered_data = filter_values(data)
            
            # Display data explorer
            file_explorer(filtered_data)
            
    except Exception as e:
        st.error(f"An error occurred: {e}")
        st.exception(e)

if __name__ == "__main__":
    main()'''

# Create sidebar navigation
st.sidebar.title("🌈 Vibe Coding")
st.sidebar.markdown("A guide to efficient AI-powered coding")

# Create the sidebar navigation menu
page = st.sidebar.radio(
    "Navigate:",
    [
        "🔯 10 Commandments",
        "🚀 Getting Started",
        "💻 Initial Dashboard",
        "📋 Prompt 1: Data Explorer",
        "📋 Prompt 2: Data Cleaning",
        "📊 Prompt 3: Preprocess Visual",
        "📊 Prompt 4: Create Visual",
        "📊 Prompt 5: Refactoring",
        "🤖 Bonus 1: AI Analytics",
        "🤖 Bonus 2: AI Agent"
    ]
)

# Main content display based on sidebar selection
if page == "🔯 10 Commandments":
    st.title("The 10 Commandments of Vibe Coding")
    st.markdown("Follow these principles to make the most of your AI-powered coding experience.")
    
    commandments = [
        "**Focus on structure, not syntax** – Don't focus on the code, focus on what the code is trying to do.",
        "**Keep it simple** – Everything from your prompt to application structure should be concise. Complexity breeds inefficiency.",
        "**Create a game plan** – Lay out your application functions before creating your tool. This way you know how to organize your prompt and what functions depend on each other.",
        "**Build incrementally** – Multiple vague instructions are the crux of vibe coding, make sure that you are building step by step.",
        "**Clean your data** – Instruct the LLM to drop and impute data based on your business understanding. Null, 0, and erroneous values must be addressed before building your app.",
        "**Build table functions before visual functions** – Create a good foundation for your visuals by first building tables that compute the values you want to present.",
        "**Be aware of dependencies** – Don't build a black box! Look at your code structure and get a firm understanding of how each function affects the other.",
        "**Refactor for efficiency** – Your code base will grow legs, if it gets too slow don't forget to refactor.",
        "**Prompt to learn** – There are no silly questions, especially when you're asking a machine.",
        "**Take risks** – Learn the way machines do: by exploring every avenue possible. Even the silly ones!"
    ]
    
    for i, commandment in enumerate(commandments, 1):
        st.markdown(f"{i}. {commandment}")
    
    # Add intro section at the top of the first page
    st.sidebar.markdown("---")
    st.sidebar.header("How to Run This App")
    st.sidebar.code("streamlit run vibe_coding_app.py", language="bash")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("Happy Vibe Coding! 🌈✨")

elif page == "🚀 Getting Started":
    st.title("Getting Started with Vibe Coding")
    
    st.header("How to Navigate Through Folders & Run Streamlit Applications")
    
    st.markdown("### 1. Open your terminal:")
    st.markdown("- On a Mac: Go to the search bar on the top right of your screen and type 'Terminal'")
    st.markdown("- On a PC: Press the Windows button and search for 'Command Prompt'")
    
    st.markdown("### 2. Check the Contents of your Directory:")
    code_mac = "ls"
    code_pc = "dir"
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Mac:**")
        st.code(code_mac, language="bash")
    with col2:
        st.markdown("**PC:**")
        st.code(code_pc, language="bash")
    
    st.markdown("### 3. Navigate into your project folder:")
    st.code("cd Documents", language="bash")
    st.code("cd VibeBoosterGPT", language="bash")
    
    st.markdown("### 4. Check the contents of your project folder:")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Mac:**")
        st.code(code_mac, language="bash")
    with col2:
        st.markdown("**PC:**")
        st.code(code_pc, language="bash")
    
    st.markdown("### 5. Run your Streamlit application:")
    st.code("streamlit run tutorial_streamlit.py", language="bash")
    
    st.markdown("### 6. If a 'Module' or 'Python Library is Missing':")
    st.code("pip install module_name", language="bash")
    
    st.header("Opening Jupyter Notebooks & Spyder")
    st.markdown("### To Open Jupyter Notebooks:")
    st.code("jupyter notebook", language="bash")
    
    st.markdown("### To Open Spyder:")
    st.code("spyder", language="bash")

elif page == "💻 Initial Dashboard":
    st.title("Initial Dashboard Setup")
    
    st.markdown("""
    Before we start building out our application with prompts, let's set up the initial dashboard. 
    This will serve as our foundation for all the enhancements we'll make through vibe coding.
    """)
    
    st.header("Step 1: Open Spyder")
    st.markdown("""
    First, let's open Spyder, a scientific Python development environment that's great for data analytics work:
    
    1. Open your terminal
    2. Type the following command:
    """)
    st.code("spyder", language="bash")
    
    st.header("Step 2: Copy the Initial Dashboard Code")
    st.markdown("""
    Next, copy the code below and paste it into the Spyder editor:
    """)
    
    with st.expander("Initial Dashboard Code", expanded=False):
        st.code(initial_dashboard_code, language="python")
    
    st.header("Step 3: Save the File")
    st.markdown("""
    Save the file with a meaningful name:
    
    1. In Spyder, go to File > Save As
    2. Navigate to your project folder
    3. Save the file as `dashboard.py`
    """)
    
    st.header("Step 4: Run the Dashboard")
    st.markdown("""
    Now let's run the dashboard:
    
    1. Open your terminal
    2. Navigate to your project directory:
    """)
    st.code("cd path/to/your/project", language="bash")
    st.markdown("""
    3. Run the Streamlit app:
    """)
    st.code("streamlit run dashboard.py", language="bash")
    
    st.markdown("""
    Congratulations! You now have a working dashboard that you can enhance using vibe coding techniques.
    Your dashboard already includes:
    
    - A file uploader for CSV data
    - A raw data viewer
    - Basic filtering functionality
    
    In the following prompts, we'll incrementally improve this dashboard with more advanced features.
    """)

elif page == "📋 Prompt 1: Data Explorer":
    st.title("Prompt 1: Data Explorer & App Foundation")
    
    with st.expander("PROMPT CONTEXT", expanded=False):
        st.markdown("""
        If you are starting a prompt from scratch, or choosing to start a new session with your chosen LLM, it is often necessary to provide the AI with context. This context should:
        1. Ask the LLM to analyze the code to understand its purpose,
        2. Provide the edit requested.
        3. Limit the LLM's interpretation
        """)
        
        st.subheader("Base Template for Prompt:")
        base_prompt = """Thoroughly analyze the streamlit application and its ingested metadata below and help me with the edits I require:

{Paste Code Here}
{Paste .info Here}

Make these edits below, but do not modify, drop or add anything else other than what I ask for here:
{Paste Prompt Here}
"""
        display_code_block(base_prompt)
    
    st.markdown("""
    Your initial prompt should allow you to explore the data about to be analyzed. By creating a file explorer you will be able to:
    - Get a feel of the data set, its contents and potential utility.
    - Detect anomalies to be cleaned such as 0s, blanks, null & erroneous values
    - Build your application in a modular fashion, allowing you to understand each step of the application's pipeline, conserving LLM compute and preventing a black box application from being engineered.
    
    Well created applications always follow the structure below:
    1. Import Libraries
    2. Load Data (either through upload or connecting to an internal file)
    3. Provide a means for data exploration & Filtration
    4. Prepare tables and calculations necessary for visuals and interactivity
    5. Combine and present all analytics in a main() function
    
    In our case a starter dashboard has already been created, which can act as your foundation for any project you choose to pursue.
    """)
    
    prompt1 = """Create a Streamlit analytics dashboard built in a modular fashion where additional functionality can be added one by one. Only create the functions and tables I request for below, do not create anything else.

Build the following modular functions:
1. Import pandas, numpy, Streamlit, Altair and all relevant libraries
2. load_data(): Use st.file_uploader() and pd.read_csv() to load a CSV. Return a DataFrame.
3. file_explorer(data): Display the raw uploaded table with st.dataframe().
4. filter_values(data): Ability to filter by value and explore the data set.
5. Create a main() function which is also wrapped by the debugger that calls the above functions in sequence and ends the app.

Here is the .info() of the data which this app will be analyzing:
# Paste df.info() output here
"""
    display_code_block(prompt1)

elif page == "📋 Prompt 2: Data Cleaning":
    st.title("Prompt 2: Data Cleaning & Imputation")
    
    with st.expander("PROMPT CONTEXT", expanded=False):
        st.markdown("""
        Before running this prompt, make sure you've already created the initial dashboard using Prompt 1. This prompt will add data cleaning functionality to your existing application.
        
        Paste your current code along with the data .info() before adding the prompt below.
        """)
    
    st.markdown("""
    Initial exploration should allow you to systematically explore your file and search for erroneous, null, blank and 0 values. At this juncture, analysts often look to create data cleaning pipelines which strategically convert these values into usable data. There are generally 3 forms of transformation analysts use:
    
    - **Statistical Imputation** – the replacement of erroneous values in the data set with the mean, median, min, max for that array. This method is often used on outliers and values likely to have been inputted incorrectly. Python will often use z scores and standard deviation to detect these outliers so be sure to be prescriptive when identifying values to impute.
    
    - **Drop** – the complete deletion of the row that erroneous value exists in. This method is used when the value is either too disruptive for analysis or was missing and so crucial that the entire row is void.
    
    - **Custom Conversion** – targeting specific values that were likely universally inputted wrong and must then be strategically edited throughout the entire data set. This can involve converting zipcodes from long form to short form, turning unique identifiers in string format to int '123456' to 123456.
    
    - **Datetime Conversion** – Turning long format date time values into python ready datetime objects which can be used for trend analysis.
    
    Clean_data() functions often require column by column instructions in order to ensure that data is addressed accordingly. This avoids python dropping entire rows when unnecessary or assuming that some transformations are valid for multiple columns when they are specifically done only for one.
    """)
    
    prompt2 = """Create a clean_data() function which acts as an automatic pipeline that cleans each column as requested below. Do not create any extra functionality, cleaning, imputation, conversion or deletion outside of what is described:

1. Total Data Set: Drop all Null Values and Blanks
2. Price: Impute all outliers with the mean of that model, make & year
3. Do not impute, edit, add or drop any values outside of those instructed above.

Create a data cleaned log in the side bar which shows how many values were dropped, imputed, converted etc. during the process.
"""
    display_code_block(prompt2)

elif page == "📊 Prompt 3: Preprocess Visual":
    st.title("Prompt 3: Preprocess for First Visual (Trend)")
    
    with st.expander("PROMPT CONTEXT", expanded=False):
        st.markdown("""
        Make sure you've already implemented the data cleaning functionality from Prompt 2. This prompt will add preprocessing for visualizations to your application.
        
        Paste your current code before adding the prompt below.
        """)
    
    st.markdown("""
    Before displaying visuals such as graphs, you must first create the table on which that visual will be created. In a streamlit pipeline this is called a 'Preprocess' or 'Pre-calculation' function. These functions automatically group data into the segments necessary to conduct analysis and then create custom columns for novel calculations unique to that analysis. Novel calculations can include rolling averages, price/sqft and even forecasted growth.
    
    It is advisable to segment your application into 'tabs' to keep your analysis organized. Both the preprocessed data and the graphs should appear in that tab.
    """)
    
    prompt3 = """1. Create a separate tab called 'Trend Analytics'
2. Create a function called preprocess_sales_trend(data) which should:
   o Create a trend analytics table with the following columns:
     ['Date', 'Dealership', 'Make', 'Model', 'Units Sold', 'Revenue'].
   o Units Sold should be the total amount of models sold in that period.
   o Revenue should be the total amount of USD generated from that model in that period. Compute revenue using price of the units sold.
   o Create a rolling 12-month average trend for Units Sold and Revenue.
   o Allow me to filter this table by date, state and dealership.
   o Output this table with filters in the 'Trend Analytics' tab.
3. Do not create any other functionality outside of the above. Keep the code simple.
"""
    display_code_block(prompt3)

elif page == "📊 Prompt 4: Create Visual":
    st.title("Prompt 4: Create a Visual – Sales Trend Over Time")
    
    with st.expander("PROMPT CONTEXT", expanded=False):
        st.markdown("""
        Make sure you've already implemented the preprocessing functionality from Prompt 3. This prompt will add visualization to your application.
        
        Paste your current code before adding the prompt below.
        """)
    
    st.markdown("""
    It is important to always separate the function which processes your data and the function which displays its visuals. This separation allows for your application to continue being modular, well organized and easily edited by an LLM.
    
    In this prompt we will specifically draw from the output of preprocess_sales_trend(data). It is important to be clear about what you want to see, how big you want that visual to be and the ultimate analytical goal of that graphic. This is true for line graphs, geospatial maps and any other form of visual representation in streamlit.
    """)
    
    prompt4 = """1. Create a function called create_trend_visuals() which ingests the output of preprocess_sales_trend(). This function should:
   o Produce a line graph in the 'Trend Analytics Tab'
   o Display the total units sold and total revenue on the same graph.
   o Have a separate axis for units sold in order to manage the scale difference between revenue and units.
   o Display the rolling 12 month trend for both units and revenue
   o Position the graph directly below the filters and above the output table of preprocess_sales_trend()
2. Do not create any functionality or visuals outside of what has been requested above. Keep the code simple.
"""
    display_code_block(prompt4)

elif page == "📊 Prompt 5: Refactoring":
    st.title("Prompt 5: Refactoring Long Code")
    
    with st.expander("PROMPT CONTEXT", expanded=False):
        st.markdown("""
        Make sure you've already implemented all the previous functionality. This prompt will help optimize your application.
        
        Paste your current code before adding the prompt below.
        """)
    
    st.markdown("""
    At this juncture, you may notice that the application is running slower than expected and that the lines of code being written are surpassing 300 or even 500 lines. This is normal in the iterative engineering process and is often a point at which a Vibe Engineer will need to begin making their code more efficient. The process of optimizing your code for performance, organization and sustainability is called refactoring. In this next prompt we will be doing the following:
    
    - **Refactoring for efficiency** - Reorganizing code structure and algorithms to achieve the same results with fewer computational resources and less time.
    
    - **Replacing for loops with vectorized operations** - Converting sequential item-by-item processing to bulk operations that process entire data arrays simultaneously, significantly increasing processing speed.
    
    - **Implementing st.cache_data and st.cache_resource** - Adding special Streamlit functions that store results of expensive calculations, preventing the need to recalculate them every time the app refreshes or when inputs haven't changed.
    
    - **Removing redundant operations** - Eliminating duplicate or unnecessary calculations and processes that consume computing resources without providing additional value to the final output.
    """)
    
    prompt5 = """Conduct the following edits on the streamlit application I pasted without losing any of the existing functionality, computations or graphic representations:
• Refactor the code base so it becomes more efficient.
• When practical, replace For Loops with Vectorized Operations.
• Implement st.cache_data and st.cache_resource
• Remove redundant operations.
"""
    display_code_block(prompt5)

elif page == "🤖 Bonus 1: AI Analytics":
    st.title("Bonus Prompt 1: Creating Generative AI Agent Analytics")
    
    with st.expander("PROMPT CONTEXT", expanded=False):
        st.markdown("""
        Make sure you've already implemented and optimized your application using the previous prompts. This prompt will add AI analytics capabilities.
        
        Paste your current code before adding the prompt below.
        """)
    
    st.markdown("""
    Generative AI Agents are one of the most powerful new tools to come from AI. These agents are capable of marrying internal analytical insights with the broader knowledge base of large language models. These agents rely on 3 key factors:
    
    - **Macro Analysis** – Like real world analysts, Generative AI agents often need to start from the macro perspective. This allows agents to look at individual data points in the context of their environment and index their performance.
    
    - **Micro Analysis** – Once a general context is provided, specific data points relevant to the insights desired must then be created. In the case of our demo file, this would be the current revenue generated of the specific make and model along with its 12 month rolling average.
    
    - **Secure API Key** – Security is paramount in Vibe Coding, and Generative AI Agents are not exempt. In order to ensure that all the context uploaded into our LLM is done so safely we must use approved API Keys.
    
    Our first prompt will generate 3 Macro Analytics tables that will be used as context in conjunction with our micro context. This will empower the user to ask questions such as 'Are sales for Toyota Camrys likely to reduce next year?'
    """)
    
    bonus_prompt1 = """Create 3 macro analytics tables that will be used as the basis for insight generation for a generative AI agent. These three tables are:
1. 12 month sales trend by Make
2. 12 month sales trend by Model
3. 12 month sales trend by State
"""
    display_code_block(bonus_prompt1)

elif page == "🤖 Bonus 2: AI Agent":
    st.title("Bonus Prompt 2: Creating the Generative AI Agent")
    
    with st.expander("PROMPT CONTEXT", expanded=False):
        st.markdown("""
        Make sure you've already implemented the macro analytics tables from Bonus Prompt 1. This prompt will create the actual AI agent.
        
        Paste your current code before adding the prompt below.
        """)
    
    st.markdown("""
    Once Micro and Macro analysis are available to be used as context, we can then create a general framework for our Generative AI agent. For the purposes of our exercise we can keep it simple, but you will generally want to include the following:
    
    1. The insight you are looking to ascertain.
    2. The Macro and Micro Analysis to be used as context.
    3. The API Key to be used.
    """)
    
    bonus_prompt2 = """Create a generative AI agent capable of predicting whether sales are likely to increase or decrease for a make, model, year combination. Use the current revenue's position in comparison to its 12 month trend for micro context and the 12 month sales trend by make, model and year as macro context.

Use OpenAI's API Infrastructure using this key:
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
"""
    display_code_block(bonus_prompt2)
    st.warning("⚠️ Note: For security reasons, never share real API keys in your applications or prompts. The key shown here is for demonstration purposes only and should be replaced with your own secure key.")