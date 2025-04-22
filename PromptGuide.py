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

# More refined professional CSS styling
st.markdown("""
<style>
    /* Base styling */
    body {
        font-family: 'Helvetica Neue', Arial, sans-serif;
        line-height: 1.6;
    }
    
    /* Header styling */
    h1 {
        color: #1E3A8A;
        margin-bottom: 1.5rem;
        padding-bottom: 0.7rem;
        border-bottom: 1px solid #e0e0e0;
        font-size: 2.2rem;
        font-weight: 600;
    }
    
    h2 {
        color: #2E4A9A;
        margin-top: 2rem;
        margin-bottom: 1rem;
        font-size: 1.8rem;
        font-weight: 500;
    }
    
    /* General text styling */
    p {
        font-size: 1.05rem;
        margin-bottom: 1rem;
        color: #333;
    }
    
    /* Command box styling */
    .prompt-block {
        background-color: #f0f4f8;
        border-left: 4px solid #1a56db;
        padding: 1.5rem;
        margin: 1.5rem 0;
        border-radius: 4px;
        font-family: 'SF Mono', 'Consolas', 'Monaco', monospace;
        white-space: pre-wrap;
        font-size: 0.95rem;
        color: #1a365d;
        line-height: 1.6;
    }
    
    /* Prompt title styling */
    .prompt-title {
        font-weight: 600;
        color: #1a56db;
        margin-bottom: 0.8rem;
        font-size: 1.1rem;
    }
    
    /* Commandment styling */
    .commandment {
        padding: 1rem;
        margin-bottom: 1rem;
        background-color: #f8fafc;
        border-radius: 6px;
        border-left: 3px solid #3b82f6;
    }
    
    .commandment-title {
        font-weight: 600;
        color: #1E3A8A;
        margin-bottom: 0.5rem;
    }
    
    /* Section styling */
    .section-title {
        font-weight: 600;
        color: #2E4A9A;
        font-size: 1.2rem;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    
    /* Lists */
    ul, ol {
        margin-bottom: 1.5rem;
    }
    
    li {
        margin-bottom: 0.5rem;
    }
    
    /* Code blocks */
    pre {
        background-color: #f1f5f9;
        padding: 1rem;
        border-radius: 4px;
        font-family: 'SF Mono', 'Consolas', 'Monaco', monospace;
        overflow-x: auto;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        font-weight: 500;
        color: #2E4A9A;
    }
    
    /* Warning styling */
    .warning {
        background-color: #fff7ed;
        border-left: 4px solid #f97316;
        padding: 1rem;
        margin: 1.5rem 0;
        border-radius: 4px;
    }
</style>
""", unsafe_allow_html=True)

# Consistent prompt context for all expanders
prompt_context = """

• Thoroughly analyze the streamlit application and its ingested metadata below and help me with the edits I require:


{Paste Code Here} 


{Paste .info Here}


• Make these edits below, but do not modify, drop or add anything else other than what I ask for here: 


{Paste Prompt Here}"""

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

# Create professional sidebar
st.sidebar.markdown("""
<div style="text-align: center; padding-bottom: 1.5rem;">
    <h1 style="color: #1E3A8A; font-size: 1.8rem; margin-bottom: 0.5rem;">🌈 Vibe Coding</h1>
    <p style="color: #64748b; font-size: 1rem; font-weight: 500;">AI-Powered Development</p>
    <hr style="margin: 1.2rem 0; border-color: #e5e7eb;">
</div>
""", unsafe_allow_html=True)

# Create the sidebar navigation menu with improved styling
page = st.sidebar.radio(
    "Navigation",
    [
        "🤖 10 Commandments of Vibe Coding",
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
if page == "🤖 10 Commandments of Vibe Coding":
    st.title("The 10 Commandments of Vibe Coding")
    
    st.markdown("""
    <p style="font-size: 1.1rem; color: #4b5563; margin-bottom: 2rem; font-style: italic;">
    Essential principles to enhance your AI-powered development workflow
    </p>
    """, unsafe_allow_html=True)
    
    commandments = [
        "**Focus on structure, not syntax** – Direct your attention to what the code accomplishes rather than its specific syntax details.",
        "**Keep it simple** – Maintain conciseness in everything from prompts to application structure. Complexity invariably leads to inefficiency.",
        "**Create a game plan** – Outline your application functions before building your tool. This strategic approach helps organize prompts and clarify function dependencies.",
        "**Build incrementally** – Employ multiple specific instructions as the foundation of vibe coding, ensuring step-by-step development progress.",
        "**Clean your data** – Guide the AI to drop and impute data based on business understanding. Address null values, zeros, and erroneous data before building your application.",
        "**Build table functions before visual functions** – Establish a solid foundation for visualizations by first creating tables that compute your target values.",
        "**Be aware of dependencies** – Avoid creating a black box! Study your code structure to thoroughly understand how functions interact with each other.",
        "**Refactor for efficiency** – As your codebase expands, remember to refactor when performance begins to degrade.",
        "**Prompt to learn** – There are no trivial questions, especially when consulting an AI system.",
        "**Take risks** – Learn as machines do: by exploring all possibilities, even those that seem unconventional."
    ]
    
    # Display commandments with improved styling - MODIFIED SECTION
    for i, commandment in enumerate(commandments, 1):
        # Extract the commandment text from the string (removing the bold markers)
        commandment_text = commandment.replace("**", "")
        # Find the first dash or hyphen to split the title from explanation
        if " – " in commandment_text:
            title, explanation = commandment_text.split(" – ", 1)
        elif " - " in commandment_text:
            title, explanation = commandment_text.split(" - ", 1)
        else:
            # If no dash is found, use the whole text as title
            title = commandment_text
            explanation = ""
        
        # Format with number and title as header, explanation as separate paragraph
        st.markdown(f"""
        <div class="commandment">
            <div class="commandment-title">{i}. {title}</div>
            <p style="margin-bottom: 0;">{explanation}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Add run instructions to sidebar with improved styling
    st.sidebar.markdown("""
    <div style="background-color: #f8fafc; padding: 1rem; border-radius: 6px; margin-top: 2rem;">
        <p style="font-weight: 600; color: #1E3A8A; margin-bottom: 0.5rem;">Quick Start</p>
        <div style="background-color: #1e293b; color: #e2e8f0; border-radius: 4px; padding: 0.8rem; font-family: monospace; font-size: 0.9rem;">
        streamlit run vibe_coding_app.py
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("""
    <div style="text-align: center; margin-top: 2rem; padding-top: 1rem; border-top: 1px solid #e5e7eb;">
        <p style="color: #3b82f6; font-weight: 500;">Happy Vibe Coding! 🌈✨</p>
    </div>
    """, unsafe_allow_html=True)

elif page == "🚀 Getting Started":
    st.title("Getting Started with Vibe Coding")
    
    st.markdown("""
    This guide will help you set up your environment and begin your Vibe Coding journey with the right tools and configuration.
    """)
    
    st.markdown("""
    <div class="section-title">Terminal Navigation</div>
    """, unsafe_allow_html=True)
    
    st.markdown("**1. Open your terminal:**")
    st.markdown("• **Mac:** Go to the search bar in the top right of your screen and type 'Terminal'")
    st.markdown("• **Windows:** Press the Windows button and search for 'Command Prompt'")
    
    st.markdown("**2. Check the Contents of your Directory:**")
    code_mac = "ls"
    code_pc = "dir"
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Mac:**")
        st.code(code_mac, language="bash")
    with col2:
        st.markdown("**Windows:**")
        st.code(code_pc, language="bash")
    
    st.markdown("**3. Navigate into your project folder:**")
    st.code("cd Documents", language="bash")
    st.code("cd VibeBoosterGPT", language="bash")
    
    st.markdown("**4. Check the contents of your project folder:**")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Mac:**")
        st.code(code_mac, language="bash")
    with col2:
        st.markdown("**Windows:**")
        st.code(code_pc, language="bash")
    
    st.markdown("**5. Run your Streamlit application:**")
    st.code("streamlit run tutorial_streamlit.py", language="bash")
    
    st.markdown("**6. If a 'Module' or 'Python Library is Missing':**")
    st.code("pip install module_name", language="bash")
    
    st.markdown("""
    <div class="section-title">Development Environments</div>
    """, unsafe_allow_html=True)
    
    st.markdown("**Jupyter Notebooks:**")
    st.code("jupyter notebook", language="bash")
    
    st.markdown("**Spyder IDE:**")
    st.code("spyder", language="bash")
    
    # Add professional tips section
    st.markdown("""
    <div class="section-title">Professional Development Practices</div>
    """, unsafe_allow_html=True)
    
    st.markdown("• **Use virtual environments** for each project to manage dependencies effectively")
    st.markdown("• **Keep your code modular** to facilitate maintenance and collaboration")
    st.markdown("• **Document your code** thoroughly with docstrings and comments")
    st.markdown("• **Commit your changes regularly** with descriptive messages if using version control")

elif page == "💻 Initial Dashboard":
    st.title("Initial Dashboard Setup")
    
    st.markdown("""
    Before enhancing our application with advanced features, we'll establish a solid foundation dashboard. This will serve as the backbone for all subsequent improvements using Vibe Coding techniques.
    """)
    
    st.markdown("""
    <div class="section-title">Step 1: Launch Your Development Environment</div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    First, let's open Spyder, a scientific Python development environment optimized for data analytics work:
    
    1. Open your terminal
    2. Execute the following command:
    """)
    st.code("spyder", language="bash")
    
    st.markdown("""
    <div class="section-title">Step 2: Implement the Initial Dashboard Code</div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    Copy the code below and paste it into the Spyder editor:
    """)
    
    with st.expander("Initial Dashboard Code", expanded=False):
        st.code(initial_dashboard_code, language="python")
    
    st.markdown("""
    <div class="section-title">Step 3: Save Your Project File</div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    Save with a Descriptive Filename:
    
    1. In Spyder, navigate to File > Save As
    2. Browse to your project directory
    3. Save the file as `dashboard.py`
    """)
    
    st.markdown("""
    <div class="section-title">Step 4: Execute Your Dashboard</div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    Now let's launch the dashboard application:
    
    1. Open your terminal
    2. Navigate to your project directory:
    """)
    st.code("cd path/to/your/project", language="bash")
    st.markdown("""
    3. Launch the Streamlit application:
    """)
    st.code("streamlit run dashboard.py", language="bash")
    
    st.markdown("""
    <div style="background-color: #f0f9ff; border-left: 4px solid #0ea5e9; padding: 1rem; margin-top: 2rem; border-radius: 4px;">
        <p style="font-weight: 600; color: #0369a1; margin-bottom: 0.5rem;">Initial Dashboard Complete</p>
        <p style="margin-bottom: 0.5rem;">You now have a functional dashboard foundation that includes:</p>
        <ul style="margin-bottom: 0; padding-left: 1.5rem;">
            <li>A CSV file uploader with error handling</li>
            <li>An interactive data viewer with expandable sections</li>
            <li>Comprehensive filtering functionality for multiple data types</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

elif page == "📋 Prompt 1: Data Explorer":
    st.title("Prompt 1: Data Explorer & App Foundation")
    
    with st.expander("PROMPT CONTEXT", expanded=False):
        st.markdown(prompt_context)
    
    st.markdown("""
    Your initial prompt should establish robust data exploration capabilities. By implementing an effective file explorer, you'll be able to:
    """)
    
    st.markdown("""
    • **Understand your dataset** – Develop intuitive familiarity with content and analytical potential
    • **Identify data issues** – Spot anomalies like null values, zeros, blanks, and outliers
    • **Build modular code** – Create transparent, well-organized application structure
    """)
    
    st.markdown("""
    <div class="section-title">Professional Application Architecture</div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    Well-designed analytics applications consistently follow this structural pattern:
    
    1. Import necessary libraries and dependencies
    2. Implement data loading mechanisms (file upload or database connection)
    3. Create data exploration and filtering capabilities
    4. Develop tables and calculations to support visualizations
    5. Integrate all components in a main() function with error handling
    """)
    
    st.markdown("""
    We've already created a starter dashboard that serves as your foundation. The following prompt will help you enhance it with robust data exploration capabilities.
    """)
    
    st.markdown("""
    <div class="prompt-title">**Prompt to Copy:**</div>
    <div class="prompt-block">
    
• Create a Streamlit analytics dashboard built in a modular fashion where additional functionality can be added one by one. Only create the functions and tables I request for below, do not create anything else.


• Build the following modular functions:
  
  
  
        • Import pandas, numpy, Streamlit, Altair and all relevant libraries
        
        • load_data(): Use st.file_uploader() and pd.read_csv() to load a CSV. Return a DataFrame.
        
        • file_explorer(data): Display the raw uploaded table with st.dataframe().
        
        • filter_values(data): Ability to filter by value and explore the data set.
        
        • Create a main() function which is also wrapped by the debugger that calls the above functions in sequence and ends the app.

• Return the entire runnable code base in one script.

• Here is the .info() of the data which this app will be analyzing:

{Paste df.info() output here}</div>
    """, unsafe_allow_html=True)

elif page == "📋 Prompt 2: Data Cleaning":
    st.title("Prompt 2: Data Cleaning & Imputation")
    
    with st.expander("PROMPT CONTEXT", expanded=False):
        st.code(prompt_context, language="markdown")
    
    st.markdown("""
    After initial exploration, you'll need to systematically address data quality issues. Professional data scientists employ strategic transformation methods to convert problematic values into usable data.
    """)
    
    st.markdown("""
    <div class="section-title">Data Cleaning Approaches</div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    • **Statistical Imputation** – Replace erroneous or missing values with statistically derived alternatives (mean, median, min, max)
    
    • **Strategic Row Removal** – Eliminate rows containing problematic values when they're too disruptive for analysis
    
    • **Custom Conversion** – Transform specific systematic errors (standardizing formats, normalizing values)
    
    • **Datetime Standardization** – Convert various datetime formats into Python-native objects for temporal analysis
    """)
    
    st.markdown("""
    Column-specific instructions are essential when implementing data cleaning to ensure appropriate treatment and prevent overzealous transformations.
    """)
    
    st.markdown("""
    <div class="prompt-title">**Prompt to Copy:**</div>
    <div class="prompt-block">

• Create a clean_data() function which acts as an automatic pipeline that cleans each column as requested below. Do not create any extra functionality, cleaning, imputation, conversion or deletion outside of what is described:

    • Total Data Set: Drop all Null Values and Blanks

    • Price: Impute all outliers with the mean of that model, make & year

    • Do not impute, edit, add or drop any values outside of those instructed above.

    • Create a data cleaned log in the side bar which shows how many values were dropped, imputed, converted etc. during the process.

• Return the entire runnable code base in one script.</div>
    """, unsafe_allow_html=True)

elif page == "📊 Prompt 3: Preprocess Visual":
    st.title("Prompt 3: Preprocess for First Visual (Trend)")
    
    with st.expander("PROMPT CONTEXT", expanded=False):
        st.code(prompt_context, language="markdown")
    
    st.markdown("""
    Before creating visual representations of your data, you must first prepare the underlying dataset structure. In professional Streamlit applications, this preparation is handled by 'preprocessing' or 'pre-calculation' functions.
    """)
    
    st.markdown("""
    • **Aggregate data** into meaningful analytical segments
    • **Generate calculated columns** specific to your analytical needs
    • **Compute advanced metrics** like rolling averages and growth rates
    • **Structure data** in formats optimized for visualization libraries
    """)
    
    st.markdown("""
    <div class="section-title">Best Practice</div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    Organize your application into logical tabs to maintain clear separation between different analytical perspectives. Each tab should contain both the preprocessed data tables and their corresponding visualizations.
    """)
    
    st.markdown("""
    <div class="prompt-title">**Prompt to Copy:**</div>
    <div class="prompt-block">

• Create a separate tab called 'Trend Analytics' to conduct trend analysis on the uploaded data.

• Create a function called preprocess_sales_trend(data) which should:

    1. Create a trend analytics table with the following columns:
    ['Date', 'Dealership', 'Make', 'Model', 'Units Sold', 'Revenue']
    2. Units Sold should be the total amount of models sold in that period.
    3. Revenue should be the total amount of USD generated from that model in that period. Compute revenue using price of the units sold.
    4. Create a rolling 12-month average trend for Units Sold and Revenue.
    
• Allow me to filter this table by date, state and dealership.

• Output this table with filters in the 'Trend Analytics' tab.

• Do not create any other functionality outside of the above. Keep the code simple.


• Return the entire runnable code base in one script.</div>
    """, unsafe_allow_html=True)

elif page == "📊 Prompt 4: Create Visual":
    st.title("Prompt 4: Create a Visual – Sales Trend Over Time")
    
    with st.expander("PROMPT CONTEXT", expanded=False):
        st.code(prompt_context, language="markdown")
    
    st.markdown("""
    In professional-grade applications, data processing and visualization are kept strictly separate. This separation enhances modularity, maintainability, and adaptability to changing requirements.
    """)
    
    st.markdown("""
    <div class="section-title">Visualization Best Practices</div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    When specifying visualization requirements, be explicit about:
    
    • **Visual type and dimensions** – Specify chart type, size, and positioning
    • **Data representation** – Clarify what data elements should be displayed and how
    • **Analytical purpose** – Articulate the insights the visualization should reveal
    • **Interactive elements** – Define what user interactions should be supported
    • **Layout considerations** – Describe how the visual relates to other UI elements
    """)
    
    st.markdown("""
    This prompt will build directly on the output from `preprocess_sales_trend(data)` created in the previous step, transforming that tabular data into compelling visual insights.
    """)
    
    st.markdown("""
    <div class="prompt-title">**Prompt to Copy:**</div>
    <div class="prompt-block">

• Create a function called create_trend_visuals() which ingests the output of preprocess_sales_trend(). This function should:

    • Produce a line graph in the 'Trend Analytics Tab'
    • Display the total units sold and total revenue on the same graph.
    • Have a separate axis for units sold in order to manage the scale difference between revenue and units.
    • Display the rolling 12 month trend for both units and revenue
    • Position the graph directly below the filters and above the output table of preprocess_sales_trend()

• Do not create any functionality or visuals outside of what has been requested above. Keep the code simple.

• Return the entire runnable code base in one script.</div>
    """, unsafe_allow_html=True)

elif page == "📊 Prompt 5: Refactoring":
    st.title("Prompt 5: Refactoring for Performance Optimization")
    
    with st.expander("PROMPT CONTEXT", expanded=False):
        st.code(prompt_context, language="markdown")
    
    st.markdown("""
    As your application evolves and expands, you may notice performance degradation and increasing code complexity. This is a natural part of the development process and signals the need for strategic optimization.
    """)
    
    st.markdown("""
    <div class="section-title">Performance Optimization Techniques</div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    • **Efficiency Refactoring** – Reorganize code structure and algorithms to achieve identical results with fewer resources
    
    • **Vectorized Operations** – Replace sequential processing with parallelized operations that handle entire data arrays simultaneously
    
    • **Streamlit Caching** – Implement specialized decorators to store results of expensive calculations
    
    • **Redundancy Elimination** – Remove duplicate calculations and unnecessary operations
    """)
    
    st.markdown("""
    <div class="prompt-title">**Prompt to Copy:**</div>
    <div class="prompt-block">
    
• Conduct the following edits on the streamlit application I pasted without losing any of the existing functionality, computations or graphic representations:

        Refactor the code base so it becomes more efficient.

        • When practical, replace For Loops with Vectorized Operations.

        • Implement st.cache_data and st.cache_resource

        • Remove redundant operations.

• Return the entire runnable code base in one script.</div>
    """, unsafe_allow_html=True)

elif page == "🤖 Bonus 1: AI Analytics":
    st.title("Bonus Prompt 1: Creating Generative AI Agent Analytics")
    
    with st.expander("PROMPT CONTEXT", expanded=False):
        st.code(prompt_context, language="markdown")
    
    st.markdown("""
    Generative AI Agents represent the cutting edge of analytical technology, combining internal data insights with the broad knowledge base of large language models.
    """)
    
    st.markdown("""
    <div class="section-title">AI Agent Components</div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    • **Macro Analysis** – Comprehensive understanding of the overall context, enabling evaluation of data points within their broader environment
    
    • **Micro Analysis** – Granular data specific to the target inquiry, such as revenue metrics for specific models with historical comparisons
    
    • **Secure Implementation** – Proper API key management and secure data handling protocols to protect sensitive information
    """)
    
    st.markdown("""
    This prompt will create three comprehensive macro analytics tables that will provide essential context for our AI agent, enabling sophisticated predictive insights.
    """)
    
    st.markdown("""
    <div class="prompt-title">**Prompt to Copy:**</div>
    <div class="prompt-block">

•  Create these three 3 macro analytics tables that will be used as the basis for insight generation for a generative AI agent: 

    • 12 month sales trend by Make
    • 12 month sales trend by Model
    • 12 month sales trend by Year

• Return the entire runnable code base in one script.</div>
    """, unsafe_allow_html=True)

elif page == "🤖 Bonus 2: AI Agent":
    st.title("Bonus Prompt 2: Creating the Generative AI Agent")
    
    with st.expander("PROMPT CONTEXT", expanded=False):
        st.code(prompt_context, language="markdown")
    
    st.markdown("""
    With both macro and micro analytical foundations in place, we can now develop a sophisticated AI agent framework. Professional implementations typically incorporate:
    """)
    
    st.markdown("""
    1. **Clearly defined analytical objectives** – Specific insights the agent should provide
    2. **Comprehensive contextual data** – Both macro trends and granular details
    3. **Secure API integration** – Properly implemented authentication and data handling
    4. **Interactive query interface** – User-friendly mechanism for posing questions
    5. **Insight visualization** – Clear presentation of the agent's analytical conclusions
    """)
    
    st.markdown("""
    <div class="warning">
        <p style="font-weight: 600; color: #c2410c; margin-bottom: 0.5rem;">Security Note</p>
        <p style="margin-bottom: 0;">For demonstration purposes, this example includes a placeholder API key. In production, always implement secure key management practices such as environment variables or secret management services.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="prompt-title">**Prompt to Copy:**</div>
    <div class="prompt-block">

•  Create a generative AI agent capable of predicting whether sales are likely to increase or decrease for a make, model, year combination. Use the current revenue's position in comparison to its 12 month trend for micro context and the 12 month sales trend by make, model and year as macro context.

•  Use OpenAI's API Infrastructure using this key:

    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

•  Return the entire runnable code base in one script.</div>
    """, unsafe_allow_html=True)