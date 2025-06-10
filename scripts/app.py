from database import extract, transform, load, drop
from read_queries import query
import streamlit as st
import plotly.express as px
import pandas as pd
from PIL import Image

# --- GLOBAL STYLES ---
def load_css():
    st.markdown("""
        <style>
            /* Modern Professional Theme for Finance Dashboard */
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
              body {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
                color: #f8fafc;
                background-color: #121212;
                -webkit-font-smoothing: antialiased;
                -moz-osx-font-smoothing: grayscale;
                line-height: 1.5;
                letter-spacing: 0.01em;
            }
            
            /* Main Container Styling */
            .main .block-container {
                background: #1e1e1e;
                border-radius: 12px;
                padding: 2.5rem 2rem;
                box-shadow: 0 8px 24px rgba(0,0,0,0.25);
                max-width: 1280px;
                margin: 0 auto;
            }
            
            /* Headings */            h1, h2, h3, h4, h5, h6 {
                color: #ffffff;
                font-weight: 700;
                letter-spacing: -0.01em;
                margin-bottom: 0.8em;
            }
            
            h1 { 
                font-size: 2.75em; 
                background: linear-gradient(90deg, #3a7bd5, #00d2ff);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
            
            h2 { font-size: 2.25em; color: #fff; }
            h3 { font-size: 1.75em; color: #fff; }
            h4 { font-size: 1.5em; color: #3a7bd5; }
            h5 { font-size: 1.25em; color: #3a7bd5; }
            h6 { font-size: 1em; color: #00d2ff; margin-bottom: 0.4em; }
              p, li {
                font-size: 1rem;
                line-height: 1.6;
                color: #d8e1f0;
            }
            
            /* Card-like styling for containers */
            .stMarkdown {
                line-height: 1.6;
            }
            
            /* Tab Navigation */
            .stTabs [data-baseweb="tab-list"] {
                gap: 2px;
                background-color: #252525;
                padding: 4px;
                border-radius: 8px;
            }
              .stTabs [data-baseweb="tab"] {
                height: 48px;
                background-color: #252525;
                border-radius: 6px;
                padding: 0 20px;
                color: #d8e1f0;
                font-weight: 500;
                transition: all 0.2s ease;
                border: none !important;
            }
            
            .stTabs [aria-selected="true"] {
                background: linear-gradient(135deg, #3a7bd5, #00d2ff);
                color: #fff;
                font-weight: 600;
                box-shadow: 0 4px 12px rgba(0, 210, 255, 0.25);
            }
            
            /* Buttons */
            .stButton>button {
                background: linear-gradient(135deg, #3a7bd5, #00d2ff);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 0.6rem 1.2rem;
                font-weight: 600;
                letter-spacing: 0.01em;
                transition: all 0.2s ease;
                box-shadow: 0 4px 12px rgba(58, 123, 213, 0.2);
            }
            
            .stButton>button:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 16px rgba(58, 123, 213, 0.3);
            }
            
            .stButton>button:active {
                transform: translateY(0);
                box-shadow: 0 4px 8px rgba(58, 123, 213, 0.2);
            }
            
            /* Form Elements */
            .stFileUploader, .stDateInput, .stRadio, .stMultiSelect, .stSelectbox {
                background: #252525;
                padding: 1rem;
                border-radius: 12px;
                border: 1px solid #333;
                margin-bottom: 1rem;
                transition: all 0.2s ease;
            }
            
            .stFileUploader:hover, .stDateInput:hover, .stRadio:hover, .stMultiSelect:hover, .stSelectbox:hover {
                border-color: #3a7bd5;
                box-shadow: 0 0 0 1px rgba(58, 123, 213, 0.2);
            }
            
            .stFileUploader label, .stDateInput label, .stRadio label, .stMultiSelect label, .stSelectbox label {
                font-weight: 500;
                color: #00d2ff;
                margin-bottom: 0.5rem;
                display: block;
            }
            
            /* Expandable sections */
            .stExpander {
                border: 1px solid #333 !important;
                border-radius: 12px !important;
                margin-bottom: 1.5rem !important;
                background: #252525 !important;
                overflow: hidden !important;
                transition: all 0.2s ease !important;
            }
            
            .stExpander:hover {
                border-color: #3a7bd5 !important;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
            }
            
            .stExpander header {
                background-color: #252525 !important;
                color: #00d2ff !important;
                font-weight: 600 !important;
                border-radius: 12px 12px 0 0 !important;
                padding: 1rem 1.2rem !important;
                border-bottom: 1px solid #333 !important;
            }
              /* Data tables */
            .stDataFrame {
                border: 1px solid #444;
                border-radius: 12px;
                background: #252525;
                overflow: hidden;
            }
            
            .stDataFrame thead th {
                background-color: #2a2a2a;
                color: #00d2ff;
                font-weight: 600;
                text-align: left;
                padding: 0.75rem 1rem !important;
                border-bottom: 2px solid #444;
            }
              .stDataFrame tbody tr {
                background-color: #252525;
                color: #ffffff;
                border-bottom: 1px solid #333;
                transition: background-color 0.15s ease;
            }
            
            .stDataFrame tbody tr:nth-child(even) {
                background-color: #2a2a2a;
            }
            
            .stDataFrame tbody tr:hover {
                background-color: #303030;
            }
            
            .stDataFrame td {
                padding: 0.75rem 1rem !important;
            }
            
            /* Metrics */
            [data-testid="stMetric"] {
                background: linear-gradient(145deg, #252525, #2a2a2a);
                border-radius: 12px;
                padding: 1.25rem;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                border: 1px solid #333;
                transition: transform 0.2s ease, box-shadow 0.2s ease;
            }
            
            [data-testid="stMetric"]:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 16px rgba(0,0,0,0.15);
                border-color: #3a7bd5;
            }
            
            [data-testid="stMetricLabel"] {
                font-weight: 600;
                color: #00d2ff;
                font-size: 0.95rem;
                letter-spacing: 0.02em;
                margin-bottom: 0.5rem;
            }
            
            [data-testid="stMetricValue"] {
                font-size: 2.25em;
                font-weight: 700;
                color: #fff;
                letter-spacing: -0.02em;
            }
            
            [data-testid="stMetricDelta"] {
                font-size: 0.9em;
                font-weight: 500;
            }
            
            /* Sidebar */
            [data-testid="stSidebar"] {
                background-color: #1a1a1a;
                border-right: 1px solid #333;
                padding: 2rem 1.5rem;
            }
            
            [data-testid="stSidebar"] h2, 
            [data-testid="stSidebar"] h3, 
            [data-testid="stSidebar"] .stMarkdown h6 {
                color: #00d2ff;
                margin-bottom: 1.5rem;
            }
              [data-testid="stSidebar"] .stRadio label {
                font-weight: 500;
                color: #ffffff;
            }
            
            /* Hide default Streamlit menu and footer */
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            
            /* Input fields styling */            div[data-testid="stDateInput"] input,
            div[data-testid="stTextInput"] input,
            div[data-testid="stNumberInput"] input {
                background-color: #303030;
                color: #ffffff;
                border: 1px solid #444;
                border-radius: 8px;
                padding: 10px 14px;
                font-size: 0.95rem;
                transition: all 0.2s ease;
            }
            
            div[data-testid="stDateInput"] input:focus,
            div[data-testid="stTextInput"] input:focus,
            div[data-testid="stNumberInput"] input:focus {
                border-color: #3a7bd5;
                box-shadow: 0 0 0 3px rgba(58, 123, 213, 0.2);
                outline: none;
            }
              div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
                background-color: #303030;
                color: #ffffff;
                border: 1px solid #444;
                border-radius: 8px;
                transition: all 0.2s ease;
                font-size: 0.95rem;
            }
            
            div[data-testid="stSelectbox"] div[data-baseweb="select"] > div:focus-within {
                border-color: #3a7bd5;
                box-shadow: 0 0 0 3px rgba(58, 123, 213, 0.2);
            }
            
            div[data-testid="stMultiSelect"] > div > div {
                background-color: #303030;
                border: 1px solid #444;
                border-radius: 8px;
                padding: 4px;
                transition: all 0.2s ease;
            }
            
            div[data-testid="stMultiSelect"] > div > div:focus-within {
                border-color: #3a7bd5;
                box-shadow: 0 0 0 3px rgba(58, 123, 213, 0.2);
            }
            
            div[data-testid="stMultiSelect"] div[data-baseweb="tag"] {
                background: linear-gradient(135deg, #3a7bd5, #00d2ff);
                color: #ffffff;
                border-radius: 6px;
                margin: 3px;
                padding: 4px 8px;
                font-size: 0.85rem;
                font-weight: 500;
            }
              div[data-testid="stMultiSelect"] input {
                color: #ffffff;
                padding: 6px;
                font-size: 0.95rem;
            }
            
            /* Custom Scrollbar */
            ::-webkit-scrollbar {
                width: 10px;
                height: 10px;
            }
            
            ::-webkit-scrollbar-track {
                background: #1a1a1a;
                border-radius: 10px;
            }
            
            ::-webkit-scrollbar-thumb {
                background: #444;
                border-radius: 10px;
                border: 2px solid #1a1a1a;
                transition: background 0.2s ease;
            }
            
            ::-webkit-scrollbar-thumb:hover {
                background: #555;
            }
            
            /* Plotly Charts Styling */
            .js-plotly-plot .plotly .main-svg {
                background-color: transparent !important;
            }
            
            .js-plotly-plot .plotly .modebar {
                background-color: rgba(26, 26, 26, 0.7) !important;
                border-radius: 8px !important;
            }
            
            .js-plotly-plot .plotly .modebar-btn path {
                fill: #00d2ff !important;
            }
            
            /* Credit Card Section Styling */
            .credit-card-section {
                margin-top: 1.5rem;
                margin-bottom: 2.5rem;
            }
            
            .credit-card-item {
                background: linear-gradient(145deg, #252525, #2a2a2a);
                border-radius: 16px;
                padding: 1.5rem;
                margin-bottom: 1.5rem;
                border: 1px solid #333;
                box-shadow: 0 4px 20px rgba(0,0,0,0.15);
                transition: transform 0.2s ease, box-shadow 0.2s ease;
            }
            
            .credit-card-item:hover {
                transform: translateY(-3px);
                box-shadow: 0 8px 30px rgba(0,0,0,0.2);
                border-color: #3a7bd5;
            }
            
            .credit-card-header {
                font-size: 1.25rem;
                font-weight: 700;
                color: #fff;
                margin-bottom: 1rem;
                border-bottom: 1px solid #444;
                padding-bottom: 0.75rem;
            }
            
            /* Progress bars */
            .stProgress > div > div > div > div {
                background-color: #3a7bd5 !important;
                background: linear-gradient(90deg, #3a7bd5, #00d2ff) !important;
            }
            
            /* Success message styling */            .stSuccess {
                background: linear-gradient(145deg, rgba(41, 171, 135, 0.1), rgba(41, 171, 135, 0.2));
                border: 1px solid rgba(41, 171, 135, 0.3);
                border-radius: 10px;
                padding: 1rem 1.25rem;
                color: #4ecca3;
            }
            
            /* Error message styling */
            .stError {
                background: linear-gradient(145deg, rgba(231, 76, 60, 0.1), rgba(231, 76, 60, 0.2));
                border: 1px solid rgba(231, 76, 60, 0.3);
                border-radius: 10px;
                padding: 1rem 1.25rem;
                color: #e74c3c;
            }
            
            /* Warning message styling */
            .stWarning {
                background: linear-gradient(145deg, rgba(241, 196, 15, 0.1), rgba(241, 196, 15, 0.2));
                border: 1px solid rgba(241, 196, 15, 0.3);
                border-radius: 10px;
                padding: 1rem 1.25rem;
                color: #f1c40f;
            }
            
            /* Info message styling */            .stInfo {
                background: linear-gradient(145deg, rgba(52, 152, 219, 0.1), rgba(52, 152, 219, 0.2));
                border: 1px solid rgba(52, 152, 219, 0.3);
                border-radius: 10px;
                padding: 1rem 1.25rem;
                color: #5dade2;
            }
        </style>
    """, unsafe_allow_html=True)

# --- PROFESSIONAL PLOTLY FIGURE STYLING ---
def styled_figure(fig, title, x_label, y_label, legend_title=None):
    fig.update_layout(
        title=dict(text=title, font=dict(size=24, color='#ffffff')),
        xaxis=dict(title=x_label, title_font=dict(size=16, color='#ffffff'), tickfont=dict(color='#f0f0f0')),
        yaxis=dict(title=y_label, title_font=dict(size=16, color='#ffffff'), tickfont=dict(color='#f0f0f0')),
        legend=dict(title=legend_title, font=dict(color='#ffffff'), bgcolor='rgba(0,0,0,0)'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=50, r=50, t=80, b=50),
        template='plotly_dark',
        hoverlabel=dict(bgcolor='#23272c', font=dict(color='#ffffff'))
    )
    return fig

def line_chart(df, x_col, y_cols, title, x_label, y_label, legend_title=None):
    fig = px.line(df, x=x_col, y=y_cols, markers=True, line_shape='spline',
                  color_discrete_sequence=px.colors.qualitative.Set2)
    return styled_figure(fig, title, x_label, y_label, legend_title)

def bar_chart(df, x_col, y_col, title, x_label, y_label, color=None, color_scale=None):
    fig = px.bar(df, x=x_col, y=y_col, color=color, color_continuous_scale=color_scale,
                 template='plotly_dark')
    if color_scale:
        fig.update_traces(marker_line_width=1.5, marker_line_color='#7ecfff')
    else:
        fig.update_traces(marker_line_width=1.5, marker_line_color='#1a73e8')
    return styled_figure(fig, title, x_label, y_label)

def pie_chart(df, values, names, title, legend_title=None, color_sequence=None):
    fig = px.pie(df, values=values, names=names, hole=0.4, color_discrete_sequence=color_sequence,
                 template='plotly_dark')
    fig.update_traces(textposition='inside', textinfo='percent+label',
                      pull=[0.05]*len(df), marker=dict(line=dict(color='#23272c', width=2)))
    fig.update_layout(title=dict(text=title, font=dict(size=24, color='#ffffff')),
                      legend=dict(title=legend_title, font=dict(color='#ffffff'), bgcolor='#23272c'))
    return fig

def main():
    # ----- PAGE SETUP -----
    st.set_page_config(
        page_title='Personal Finance Dashboard',
        page_icon=':money_with_wings:',
        layout='wide',
        initial_sidebar_state='expanded'
    )
    load_css()

    # ----- TITLE & TABS -----
    st.title('Personal Finance Dashboard')
    tab1, tab2, tab3, tab4 = st.tabs(['Home', 'Data', 'Dashboard', 'Documentation'])    # ----- SIDE BAR -----
    with st.sidebar:
        st.header('Filters')
        column_options = ['binance', 'gcash', 'grabpay', 'maya', 'ronin', 'seabank', 'shopeepay', 'unionbank', 'wallet', 'net_worth']
        selected_columns = st.multiselect('Select accounts to display:', column_options, default=['net_worth'])
        view = st.radio("Select view:", ["monthly", "weekly", "daily"], index=0, horizontal=True, key="sidebar")

    # ----- HOME TAB -----
    with tab1:
        with st.container():
            st.subheader('Project Overview')
            st.markdown("""
                The Personal Finance Dashboard takes your expenditure data from the Bluecoins app and transforms it 
                into an interactive dashboard to help you manage your money better. Bluecoins is an expense tracking 
                app that lets you export your financial records as a CSV file. The Personal Finance Dashboard accepts 
                this file—or any other CSV file with a similar format—to generate detailed analytics, so you can see 
                exactly where your rupees are going and make smarter budgeting decisions.
            """)
            try:
                personal_finance = Image.open('images/finance.jpg')
                st.image(personal_finance, caption='Source: LittlePigPower/Shutterstock.com', use_container_width=True)
            except FileNotFoundError:
                st.warning("Image not found")

        with st.container():
            st.subheader('Motivation Behind the Project')
            st.markdown("""
                As an Indian student, managing my finances has always been a challenge—especially 
                with limited pocket money and the need to balance studies, personal life, and unexpected expenses. 
                For over a year, I’ve used the Bluecoins app to keep track of every rupee spent and earned. Now,
                I want to go beyond just recording transactions and uncover meaningful insights from my own data.
                With this project, I aim to answer key questions about my spending and income habits:

                - **Where do I spend the most rupees?**  
                Identifying my biggest expenses helps me prioritize and adjust my habits.
                - **What should my daily, weekly, and monthly budget look like in rupees?**  
                Using my actual spending patterns, I want to set realistic and sustainable budgets in ₹.
                - **Where does most of my money come from?**  
                Understanding my income sources helps me plan better for the future.
                - **What are my most preferred payment and receiving methods?**  
                Knowing which methods I use most often can help me streamline my finances.
                - **How much money moves in and out of my accounts over time in rupees?**  
                Tracking cash flow trends ensures I stay on top of my financial health.

                This project is also a chance for me to apply what I’ve learned as a computer science student. I’ve used:

                - **Python** (including Pandas for data analysis, SQLAlchemy for database integration, Plotly for visualizations, and Streamlit for the web interface)
                - **SQL** (relational databases and writing queries)
                - **Git workflow** (version control and collaboration)
                - **Project management and documentation** (to keep everything organized and reproducible)
                By building this financial tracker, I hope to not only manage my money better but also grow my skills in programming, data analysis, and web development—while keeping every rupee in check!
            """)
            try:
                architecture_diagram = Image.open('images/Architecture Diagram.jpg')
                st.image(architecture_diagram, caption='Technologies used', use_container_width=True)
            except FileNotFoundError:
                st.warning("Image not found")

        with st.container():
            st.subheader('Get Started')
            st.markdown("""
                To use the app, kindly follow these instructions:

                1. Export transactions data from Bluecoins app. This will create a file called ‘transactions_list.csv’.
                2. Go to the ‘Data’ tab and upload the file. The dashboard is created automatically once the file is uploaded. Dataframes containing raw and derived data are also shown. You can explore the data by clicking on the expanders.
                3. Go to the ‘Dashboard’ tab and explore the charts. Use the filters on the left sidebar to show specific plots or views.
            """)

    # ----- DATA TAB -----
    with tab2:
        connection_uri = "postgresql://postgres:password@postgres:5432/personal_finance_dashboard"
        file = st.file_uploader("Upload file here", type=['csv'])

        if file is not None:
            if st.button("Generate Dashboard"):
                try:
                    raw_transactions = extract(file)
                    load(raw_transactions, "raw_transactions", connection_uri)
                    cleaned_transactions = transform(raw_transactions)
                    load(cleaned_transactions, "transactions", connection_uri)
                    st.success("Dashboard generated successfully!")
                except Exception as e:
                    st.error(f"Error generating dashboard: {str(e)}")
        else:
            st.warning("Please upload a CSV file to proceed.")

        if st.button("Clear Data"):
            try:
                drop("raw_transactions", connection_uri)
                drop("transactions", connection_uri)
                st.success("Data cleared successfully!")
            except Exception as e:
                st.error(f"Error clearing data: {str(e)}")

        with st.expander('Raw Transactions Data'):
            try:
                raw_transactions = query("raw_transactions")
                st.dataframe(raw_transactions, height=400, use_container_width=True)
            except Exception as e:
                st.error(f"Error loading raw transactions: {str(e)}")

        with st.expander('Cleaned Transactions Data'):
            try:
                cleaned_transactions = query("transactions")
                st.dataframe(cleaned_transactions, height=400, use_container_width=True)
            except Exception as e:
                st.error(f"Error loading cleaned transactions: {str(e)}")

        with st.expander('Accounts Data'):
            try:
                accounts = query("daily_amount_over_time")
                st.dataframe(accounts, height=400, use_container_width=True)
            except Exception as e:
                st.error(f"Error loading accounts data: {str(e)}")

    # ----- DASHBOARD TAB -----
    with tab3:
        try:
            # Account Balance Over Time
            if view == 'monthly':
                monthly_amount_over_time = query("monthly_amount_over_time")
                fig = line_chart(
                    monthly_amount_over_time, 'month', selected_columns,
                    'Account Balance Over Time', 'Month', 'Amount (₹)', 'Account'
                )
            elif view == 'weekly':
                weekly_amount_over_time = query("weekly_amount_over_time")
                fig = line_chart(
                    weekly_amount_over_time, 'week', selected_columns,
                    'Account Balance Over Time', 'Week', 'Amount (₹)', 'Account'
                )
            elif view == 'daily':
                daily_amount_over_time = query("daily_amount_over_time")
                fig = line_chart(
                    daily_amount_over_time, 'day', selected_columns,
                    'Account Balance Over Time', 'Day', 'Amount (₹)', 'Account'
                )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("---")

            # Monthly Cash Flow Bar Graph
            if view == 'monthly':
                try:
                    monthly_cash_flow = query("monthly_cash_flow")
                    fig = bar_chart(
                        monthly_cash_flow, 'month', 'cash_flow',
                        'Monthly Cash Flow (Income - Expenses)', 'Month', 'Cash Flow (₹)',
                        color='cash_flow', color_scale='bluered'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                except Exception as e:
                    st.error(f"Error loading monthly cash flow: {str(e)}")
            st.markdown("---")

            # Payment & Receiving Methods
            b1, b2 = st.columns(2)
            with b1:
                payment_methods = query("payment_methods")
                fig = bar_chart(
                    payment_methods, 'account', 'amount',
                    'Payment Methods', 'Account', 'Amount (₹)'
                )
                st.plotly_chart(fig, use_container_width=True)
            with b2:
                receiving_methods = query("receiving_methods")
                fig = bar_chart(
                    receiving_methods, 'account', 'amount',
                    'Receiving Methods', 'Account', 'Amount (₹)'
                )
                st.plotly_chart(fig, use_container_width=True)
            st.markdown("---")            # Expenses & Income by Category (Pie Charts)
            c1, c2 = st.columns(2)
            with c1:
                expenses_per_category = query("expenses_per_category")
                fig = pie_chart(
                    expenses_per_category, 'expenses', 'category',
                    'Expenses Per Category', 'Category', px.colors.sequential.RdPu_r
                )
                st.plotly_chart(fig, use_container_width=True)
            with c2:
                income_per_category = query("income_per_category")
                fig = pie_chart(
                    income_per_category, 'income', 'category',
                    'Income Per Category', 'Category', px.colors.sequential.GnBu_r
                )
                st.plotly_chart(fig, use_container_width=True)
            st.markdown("---")

            # Top Expenses & Income Sources (Tables)
            d1, d2 = st.columns(2)
            with d1:
                st.markdown("###### Top Expenses")
                st.dataframe(expenses_per_category, height=400, use_container_width=True)
            with d2:
                st.markdown("###### Top Income Sources")
                st.dataframe(income_per_category, height=400, use_container_width=True)
            st.markdown("---")

            # Expenses Over Time
            if view == 'monthly':
                monthly_expenses = query("monthly_expenses")
                fig = line_chart(
                    monthly_expenses, 'month', 'expenses',
                    'Monthly Expenses', 'Month', 'Amount (₹)'
                )
            elif view == "weekly":
                weekly_expenses = query("weekly_expenses")
                fig = line_chart(
                    weekly_expenses, 'week', 'expenses',
                    'Weekly Expenses', 'Week', 'Amount (₹)'
                )
            elif view == "daily":
                daily_expenses = query("daily_expenses")
                fig = line_chart(
                    daily_expenses, 'day', 'expenses',
                    'Daily Expenses', 'Day', 'Amount (₹)'
                )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("---")

            # Credit Card Summary Section
            st.subheader("Credit Card Summary")
            try:
                # Execute the query with enhanced error handling
                credit_cards_df = query("credit_card_summary")
                
                if not credit_cards_df.empty:
                    # Make sure columns exist and are properly typed
                    if 'card_name' in credit_cards_df.columns and 'spent' in credit_cards_df.columns and 'limit' in credit_cards_df.columns:
                        # Explicitly convert columns to ensure proper types
                        credit_cards_df['spent'] = pd.to_numeric(credit_cards_df['spent'], errors='coerce').fillna(0.0)
                        credit_cards_df['limit'] = pd.to_numeric(credit_cards_df['limit'], errors='coerce').fillna(50000.0)
                        
                        st.markdown("Enter or adjust the credit limit for each card below:")

                        for idx, row in credit_cards_df.iterrows():
                            card_name = row['card_name']
                            spent_amount = float(row['spent'])  # Ensure it's a float
                            
                            session_key_limit = f"credit_limit_{card_name}"
                            default_placeholder_limit = 50000.0

                            # Initialize session state for this card's limit if not already set by user
                            if session_key_limit not in st.session_state:
                                st.session_state[session_key_limit] = default_placeholder_limit
                            
                            st.markdown(f"#### {card_name}")
                            
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                st.metric(label="Spent This Month", value=f"₹{spent_amount:,.0f}")
                            
                            with col2:
                                # User input for limit, value from session state
                                current_limit_for_input = float(st.session_state[session_key_limit])
                                user_defined_limit = st.number_input(
                                    f"Credit Limit", # Label is simpler as card name is in header
                                    min_value=0.0,
                                    value=current_limit_for_input,
                                    step=1000.0,
                                    key=f"input_{session_key_limit}", # Unique key for the input widget
                                    help="Enter the total credit limit for this card."
                                )
                                # If user changes the limit, update session state and rerun
                                if user_defined_limit != current_limit_for_input:
                                    st.session_state[session_key_limit] = user_defined_limit
                                    st.experimental_rerun()
                            
                            limit_left = user_defined_limit - spent_amount
                            with col3:
                                delta_color = "normal"
                                if limit_left < 0:
                                    delta_color = "inverse"
                                elif limit_left < (user_defined_limit * 0.1): # If less than 10% limit left
                                    delta_color = "off" # Typically red for 'off' in default theme
                                    
                                st.metric(label="Limit Left", value=f"₹{limit_left:,.0f}", delta_color=delta_color)
                            st.markdown("---")

                        # Display horizontal bar graphs for spend vs. limit
                        st.markdown("##### Credit Card Utilization")
                        
                        for idx, row in credit_cards_df.iterrows():
                            card_name = row['card_name']
                            spent_amount = float(row['spent'])
                            user_limit = float(st.session_state.get(f"credit_limit_{card_name}", 50000.0))
                            
                            # Calculate utilization percentage
                            utilization_pct = min(100, (spent_amount / user_limit * 100)) if user_limit > 0 else 0
                            
                            # Create a DataFrame for the horizontal bar chart
                            util_df = pd.DataFrame({
                                'Category': ['Spent', 'Available'],
                                'Amount': [spent_amount, max(0, user_limit - spent_amount)],
                                'Color': ['#e57373', '#81c784']  # Red for spent, green for available
                            })
                            
                            st.markdown(f"**{card_name}** - {utilization_pct:.1f}% utilized")
                            
                            # Create horizontal bar chart
                            fig = px.bar(
                                util_df, 
                                y='Category', 
                                x='Amount', 
                                color='Color',
                                color_discrete_map={'#e57373': '#e57373', '#81c784': '#81c784'},
                                orientation='h',
                                barmode='stack',
                                height=100,
                                template='plotly_dark'
                            )
                            
                            # Update layout for a cleaner look
                            fig.update_layout(
                                showlegend=False,
                                margin=dict(l=0, r=10, t=10, b=0),
                                xaxis=dict(
                                    title=None,
                                    showgrid=False,
                                    tickformat='₹,.0f'
                                ),
                                yaxis=dict(
                                    title=None,
                                    showgrid=False
                                ),
                                plot_bgcolor='rgba(0,0,0,0)',
                                paper_bgcolor='rgba(0,0,0,0)'
                            )
                            
                            # Add annotations for amounts
                            fig.add_annotation(
                                x=spent_amount/2,
                                y='Spent',
                                text=f"₹{spent_amount:,.0f}",
                                showarrow=False,
                                font=dict(color='white', size=12)
                            )
                            
                            available = max(0, user_limit - spent_amount)
                            if available > 0:
                                fig.add_annotation(
                                    x=spent_amount + available/2,
                                    y='Available',
                                    text=f"₹{available:,.0f}",
                                    showarrow=False,
                                    font=dict(color='white', size=12)
                                )
                            
                            st.plotly_chart(fig, use_container_width=True)
                            st.markdown("---")
                    else:
                        st.warning("Credit card data structure is not in the expected format. Please check the database query.")
                else:
                    st.info("No credit card transactions found for the current month to summarize.")
            except Exception as e:
                st.error(f"Error loading credit card summary: {str(e)}")
                import traceback
                st.error(traceback.format_exc())
            st.markdown("---")

            # Calendar Day Picker
            st.subheader("View Transactions by Day")
            selected_date = st.date_input("Select a date to view transactions", key="calendar")
            if selected_date:
                try:
                    day_transactions = query("transactions_by_date", date=selected_date)
                    
                    # Create bar graphs for income and expense transactions of the selected day
                    if not day_transactions.empty:
                        # Create a copy to avoid modifying the original dataframe
                        day_transactions_analysis = day_transactions.copy()
                        
                        # Display the transactions table
                        st.dataframe(day_transactions, height=400, use_container_width=True)
                        
                        # Split transactions into income and expense
                        st.markdown("### Transactions Summary for Selected Day")
                        daily_bar_cols = st.columns(2)
                        
                        with daily_bar_cols[0]:
                            # Income transactions
                            income_transactions = day_transactions_analysis[day_transactions_analysis['type'] == 'income']
                            if not income_transactions.empty:
                                # Group by category for visualization
                                income_by_category = income_transactions.groupby('category')['amount'].sum().reset_index()
                                income_by_category['amount'] = income_by_category['amount'].abs()  # Ensure positive values
                                
                                fig_income = px.bar(
                                    income_by_category,
                                    x='category',
                                    y='amount',
                                    title=f'Income on {selected_date.strftime("%d %b, %Y")}',
                                    color_discrete_sequence=['#81c784'],  # Green shade for income
                                    template='plotly_dark'
                                )
                                fig_income = styled_figure(
                                    fig_income, 
                                    f'Income on {selected_date.strftime("%d %b, %Y")}', 
                                    'Category', 
                                    'Amount (₹)'
                                )
                                st.plotly_chart(fig_income, use_container_width=True)
                                
                                # Show total income
                                total_income = income_by_category['amount'].sum()
                                st.metric("Total Income", f"₹{total_income:,.2f}", delta_color="normal")
                            else:
                                st.info(f"No income transactions found on {selected_date.strftime('%d %b, %Y')}")
                        
                        with daily_bar_cols[1]:
                            # Expense transactions
                            expense_transactions = day_transactions_analysis[day_transactions_analysis['type'] == 'expense']
                            if not expense_transactions.empty:
                                # Group by category for visualization
                                expense_by_category = expense_transactions.groupby('category')['amount'].sum().reset_index()
                                expense_by_category['amount'] = expense_by_category['amount'].abs()  # Convert to positive for visualization
                                
                                fig_expense = px.bar(
                                    expense_by_category,
                                    x='category',
                                    y='amount',
                                    title=f'Expenses on {selected_date.strftime("%d %b, %Y")}',
                                    color_discrete_sequence=['#e57373'],  # Red shade for expenses
                                    template='plotly_dark'
                                )
                                fig_expense = styled_figure(
                                    fig_expense, 
                                    f'Expenses on {selected_date.strftime("%d %b, %Y")}', 
                                    'Category', 
                                    'Amount (₹)'
                                )
                                st.plotly_chart(fig_expense, use_container_width=True)
                                
                                # Show total expense
                                total_expense = expense_by_category['amount'].sum()
                                st.metric("Total Expenses", f"₹{total_expense:,.2f}", delta_color="inverse")
                            else:
                                st.info(f"No expense transactions found on {selected_date.strftime('%d %b, %Y')}")
                        
                        # Net cashflow for the day
                        if not income_transactions.empty or not expense_transactions.empty:
                            total_income = income_transactions['amount'].sum() if not income_transactions.empty else 0
                            total_expense = expense_transactions['amount'].abs().sum() if not expense_transactions.empty else 0
                            net_cashflow = total_income - total_expense
                            
                            delta_color = "normal" if net_cashflow >= 0 else "inverse"
                            st.metric(
                                label=f"Net Cashflow on {selected_date.strftime('%d %b, %Y')}", 
                                value=f"₹{net_cashflow:,.2f}", 
                                delta_color=delta_color
                            )
                    else:
                        st.info(f"No transactions found for {selected_date.strftime('%d %b, %Y')}")
                    
                except Exception as e:
                    st.error(f"Error loading transactions for {selected_date}: {str(e)}")
        except Exception as e:
            st.error(f"Error in dashboard: {str(e)}")

    # ----- DOCUMENTATION TAB -----
    with tab4:
        st.subheader('Architecture Diagram')
        try:
            architecture_diagram = Image.open('images/Architecture Diagram.jpg')
            st.image(architecture_diagram, use_container_width=True)
        except FileNotFoundError:
            st.warning("Image not found")

        st.subheader('How It Works')
        try:
            workflow = Image.open('images/workflow.png')
            st.image(workflow, use_container_width=True)
        except FileNotFoundError:
            st.warning("Image not found")

if __name__ == '__main__':
    main()
