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
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                color: #e0e0e0;
                background-color: #181a1b;
            }
            .main .block-container {
                background: #23272c;
                border-radius: 12px;
                padding: 2rem 1.5rem;
                box-shadow: 0 2px 8px rgba(0,0,0,0.25);
            }
            h1, h2, h3, h4, h5, h6 {
                color: #e0e0e0;
                font-weight: 700;
            }
            h1 { font-size: 2.5em; margin-bottom: 0.5em; }
            h2 { font-size: 2em; margin-bottom: 0.4em; }
            h3 { font-size: 1.75em; margin-bottom: 0.3em; }
            h6 { font-size: 1.25em; margin-bottom: 0.2em; color: #7ecfff; }
            .stTabs [data-baseweb="tab-list"] {
                gap: 12px;
            }
            .stTabs [data-baseweb="tab"] {
                height: 44px;
                background-color: #23272c;
                border-radius: 6px 6px 0 0;
                padding: 10px 16px;
                color: #b0b8c1;
                font-weight: 500;
            }
            .stTabs [aria-selected="true"] {
                background-color: #1a73e8;
                color: #fff;
                font-weight: 700;
            }
            .stButton>button {
                border: 2px solid #1a73e8;
                border-radius: 0.375rem;
                color: #1a73e8;
                background-color: #23272c;
                padding: 0.5rem 1rem;
                font-weight: 600;
                transition: all 0.2s;
            }
            .stButton>button:hover {
                border-color: #7ecfff;
                color: #23272c;
                background-color: #7ecfff;
            }
            .stButton>button:active {
                border-color: #0056b3 !important;
                background-color: #0056b3 !important;
                color: #fff !important;
            }
            .stFileUploader label, .stDateInput label, .stRadio label, .stMultiSelect label {
                font-weight: 500;
                color: #7ecfff;
            }
            .stExpander {
                border: 1px solid #333 !important;
                border-radius: 0.375rem !important;
                margin-bottom: 1rem !important;
                background: #23272c !important;
            }
            .stExpander header {
                background-color: #23272c !important;
                color: #7ecfff !important;
                font-weight: 600 !important;
                border-radius: 0.375rem 0.375rem 0 0 !important;
                padding: 0.75rem 1rem !important;
            }
            .stDataFrame {
                border: 1px solid #333;
                border-radius: 0.375rem;
                background: #23272c;
            }
            .stDataFrame thead th {
                background-color: #23272c;
                color: #7ecfff;
                font-weight: 700;
                text-align: left;
            }
            .stDataFrame tbody tr {
                background-color: #23272c;
                color: #e0e0e0;
            }
            .stDataFrame tbody tr:nth-child(even) {
                background-color: #202124;
            }
            .stDataFrame tbody tr:hover {
                background-color: #1a1d1f;
            }
            [data-testid="stMetric"] {
                background-color: #23272c;
                border: 1px solid #333;
                border-radius: 0.375rem;
                padding: 1rem;
                box-shadow: 0 2px 4px rgba(0,0,0,0.15);
            }
            [data-testid="stMetricLabel"] {
                font-weight: 600;
                color: #7ecfff;
            }
            [data-testid="stMetricValue"] {
                font-size: 2em;
                font-weight: 700;
                color: #e0e0e0;
            }
            [data-testid="stMetricDelta"] {
                font-size: 0.9em;
            }
            [data-testid="stSidebar"] {
                background-color: #23272c;
                padding: 1rem;
            }
            [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] .stMarkdown h6 {
                 color: #7ecfff;
            }
            /* Hide default Streamlit menu and footer */
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)
    st.markdown(
        "<hr><div style='text-align:center; color:#7ecfff; margin-top:2rem;'>Powered by Personal Finance Dashboard © 2025</div>",
        unsafe_allow_html=True
    )

# --- PROFESSIONAL PLOTLY FIGURE STYLING ---
def styled_figure(fig, title, x_label, y_label, legend_title=None):
    fig.update_layout(
        title=dict(text=title, font=dict(size=24, color='#e0e0e0')),
        xaxis=dict(title=x_label, title_font=dict(size=16, color='#e0e0e0'), tickfont=dict(color='#e0e0e0')),
        yaxis=dict(title=y_label, title_font=dict(size=16, color='#e0e0e0'), tickfont=dict(color='#e0e0e0')),
        legend=dict(title=legend_title, font=dict(color='#e0e0e0'), bgcolor='#23272c'),
        plot_bgcolor='#23272c',
        paper_bgcolor='#23272c',
        margin=dict(l=50, r=50, t=80, b=50),
        template='plotly_dark',
        hoverlabel=dict(bgcolor='#23272c', font=dict(color='#e0e0e0'))
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
    fig.update_layout(title=dict(text=title, font=dict(size=24, color='#e0e0e0')),
                      legend=dict(title=legend_title, font=dict(color='#e0e0e0'), bgcolor='#23272c'))
    return fig

def main():
    # ----- PAGE SETUP -----
    st.set_page_config(
        page_title='Personal Finance Dashboard',
        page_icon=':money_with_wings:',
        layout='wide'
    )
    load_css()

    # ----- TITLE & TABS -----
    st.title('Personal Finance Dashboard')
    tab1, tab2, tab3, tab4 = st.tabs(['Home', 'Data', 'Dashboard', 'Documentation'])

    # ----- SIDE BAR -----
    with st.sidebar:
        st.header('Filters')
        column_options = ['binance', 'gcash', 'grabpay', 'maya', 'ronin', 'seabank', 'shopeepay', 'unionbank', 'wallet', 'net_worth']
        selected_columns = st.multiselect('Select accounts to display:', column_options, default=['net_worth'])
        view = st.radio("Select view:", ["monthly", "weekly", "daily"], index=1, horizontal=True, key="sidebar")

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

            # Recent Net Daily Summary (Last 7 Days)
            daily_summary_30 = query("daily_net_summary_last_n_days")
            daily_summary_30['date'] = pd.to_datetime(daily_summary_30['date'])
            today = pd.Timestamp.today().normalize()
            last_7_dates = pd.date_range(end=today, periods=7)
            daily_summary_7 = pd.DataFrame({'date': last_7_dates})
            daily_summary_7 = daily_summary_7.merge(
                daily_summary_30[['date', 'net_amount']], on='date', how='left'
            ).fillna(0)
            daily_summary_7['day'] = daily_summary_7['date'].dt.strftime('%a')
            avg_7 = daily_summary_7['net_amount'].mean()
            avg_30 = daily_summary_30['net_amount'].mean()

            fig = bar_chart(
                daily_summary_7, 'day', 'net_amount',
                'Daily Net Amount (Last 7 Days)', 'Day', 'Net Amount (₹)'
            )
            fig.add_hline(
                y=avg_7, line_dash='dash', line_color='#7ecfff',
                annotation_text='7-day avg', annotation_position='top left'
            )
            fig.add_hline(
                y=avg_30, line_dash='dash', line_color='#1a73e8',
                annotation_text='30-day avg', annotation_position='bottom left'
            )
            st.plotly_chart(fig, use_container_width=True)
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
            st.markdown("---")

            # Expenses & Income by Category (Pie Charts)
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

            # Calendar Day Picker
            st.subheader("View Transactions by Day")
            selected_date = st.date_input("Select a date to view transactions", key="calendar")
            if selected_date:
                try:
                    day_transactions = query("transactions_by_date", date=selected_date)
                    st.dataframe(day_transactions, height=400, use_container_width=True)
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
