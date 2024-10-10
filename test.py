import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

try:
    import statsmodels.api as sm
    STATSMODELS_AVAILABLE = True
except ImportError:
    STATSMODELS_AVAILABLE = False

# Set page config
st.set_page_config(page_title="2018 Happiness Index Explorer", layout="wide", initial_sidebar_state="expanded")


st.markdown("""
<style>
    .reportview-container {
        background: #f0f2f6;
    }
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 5rem;
        padding-right: 5rem;
    }
    h1 {
        color: #1E3888;
    }
    h2 {
        color: #47A8BD;
    }
    .stButton>button {
        color: #ffffff;
        background-color: #47A8BD;
        border-radius: 5px;
    }
    .stSelectbox [data-baseweb="select"] {
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
    .stMultiSelect [data-baseweb="select"] {
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Load the data function
@st.cache_data
def load_data():
    try:
        data = pd.read_csv("https://github.com/reeyyyxd/introduction/raw/refs/heads/main/2018.csv")
        return data
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return None



def main():
    # Load data and verify
    df = load_data()
    if df is None:
        st.error("Data could not be loaded. Please check the load_data function.")
        return  # Exit if data is not loaded

    url = "https://www.kaggle.com/datasets/sougatapramanick/happiness2018"

    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Introduction", "Data Overview", "Factor Analysis", "Country Comparison", "Conclusion"])

    if page == "Introduction":
        st.title("Data Exploration: 2018 Happiness Index")
        st.write("""
        	Sourced from the World Happiness Report in the year 2018, 
        	it compiles data from surveys conducted by various organizations. 
        	The dataset is about the insights into the factors that contribute to happiness across various countries and regions. 
        	The data includes the following multiple variables listed below:

        **Key Variables:**
        - Overall rank
        - Country or region
        - **Score (Happiness Score)** - Independent Variable
        - **GDP per capita** - Dependent Variable
        - **Social support** - Dependent Variable
        - **Healthy life expectancy** - Dependent Variable
        - **Freedom to make life choices** - Dependent Variable
        - **Generosity** - Dependent Variable
        - **Perceptions of corruption** - Dependent Variable
        
        


        """)
        st.markdown("You can check out the dataset and details from the Kaggle [link here.](%s)" % url)




    elif page == "Data Overview":
        st.title("Data Overview")

        st.subheader("Sample Data")
        st.write("This is the raw dataset shown below:")
        st.dataframe(df)

        st.subheader("Missing Data")
        st.write("Checking for missing values in the dataset:")
        missing_data = df.isna().sum()
        st.dataframe(missing_data[missing_data > 0])

        # Function to detect and display outliers
    def detect_outliers(df, column):
        upper_limit = df[column].mean() + 3 * df[column].std()
        lower_limit = df[column].mean() - 3 * df[column].std()
        outliers = df[(df[column] > upper_limit) | (df[column] < lower_limit)]
        return outliers

    st.subheader("Outliers Detection")
    st.write("The following rows are considered outliers for each variable:")

    columns_to_check = ["Score", "GDP per capita", "Social support", 
                        "Healthy life expectancy", "Freedom to make life choices", 
                        "Generosity", "Perceptions of corruption"]

    for col in columns_to_check:
        outliers = detect_outliers(df, col)
        if not outliers.empty:
            st.write(f"Outliers in '{col}':")
            st.dataframe(outliers)
        else:
            st.write(f"No outliers detected in '{col}'.")

    def remove_outliers(df, column):
        upper_limit = df[column].mean() + 3 * df[column].std()
        lower_limit = df[column].mean() - 3 * df[column].std()
        return df[(df[column] >= lower_limit) & (df[column] <= upper_limit)]

        df_clean = df.copy()
        for col in columns_to_check:
        df_clean = remove_outliers(df_clean, col)

        st.subheader("Before and After Removing Outliers")
        st.write(f"Number of rows before removing outliers: {df.shape[0]}")
        st.write(f"Number of rows after removing outliers: {df_clean.shape[0]}")
        st.write(f"**We didn't apply the cleaned dataset onwards so all countries will be included.**")

        st.subheader("Summary Statistics")
        st.dataframe(df.drop(columns=["Overall rank"]).describe())


        st.subheader("Distribution of Happiness Scores")
        st.write("This displays the frequency distribution of happiness scores, showing how many countries fall into each score range.")
        fig_dist = px.histogram(df, x="Score", nbins=20, color_discrete_sequence=['#47A8BD'])
        fig_dist.update_layout(title_text="Distribution of Happiness Scores", title_x=0.5)
        st.plotly_chart(fig_dist, use_container_width=True)

    elif page == "Factor Analysis":
        st.title("Factor Analysis")

        # Select only numeric columns for correlation analysis
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        numeric_cols.remove('Overall rank')  # Remove Overall rank from factors
        numeric_cols.remove('Score')  # Remove Score from factors

        st.subheader("Correlation Between Factors")
        corr_matrix = df[numeric_cols + ['Score']].corr()

        fig_corr = px.imshow(corr_matrix, text_auto=True, aspect="auto", color_continuous_scale='RdBu_r')
        fig_corr.update_layout(title_text="Correlation Heatmap", title_x=0.5)
        st.plotly_chart(fig_corr, use_container_width=True)

        st.subheader("Factor Impact on Happiness")
        factor = st.selectbox("Select a factor to analyze:", numeric_cols)

        fig_scatter = px.scatter(df, x=factor, y="Score", hover_data=['Country or region'], color_discrete_sequence=['#47A8BD'])

        if STATSMODELS_AVAILABLE:
            fig_scatter.update_traces(mode='markers+text', textposition='top center')
            fig_scatter.add_trace(
                px.scatter(df, x=factor, y="Score", trendline="ols").data[1]
            )
        else:
            st.warning("Note: Trendline is not available due to missing 'statsmodels' library.")

        fig_scatter.update_layout(title_text=f"{factor} vs Happiness Score", title_x=0.5)
        st.plotly_chart(fig_scatter, use_container_width=True)



    elif page == "Country Comparison":
        st.title("Country Comparison")
        countries = st.multiselect("Select countries to compare:", df['Country or region'].unique(), default=df['Country or region'].unique()[:3])

        if not countries:
            st.warning("Please select at least one country.")
        else:
            comparison_data = df[df['Country or region'].isin(countries)]

            fig = make_subplots(rows=2, cols=3,
                                subplot_titles=("GDP per capita", "Social support", "Healthy life expectancy",
                                                "Freedom to make life choices", "Generosity", "Perceptions of corruption"))

            factors = ["GDP per capita", "Social support", "Healthy life expectancy",
                       "Freedom to make life choices", "Generosity", "Perceptions of corruption"]

            for i, factor in enumerate(factors):
                fig.add_trace(go.Bar(x=comparison_data['Country or region'], y=comparison_data[factor], name=factor),
                              row=(i // 3) + 1, col=(i % 3) + 1)

            fig.update_layout(height=800, title_text="Comparison of Happiness Factors Across Selected Countries", title_x=0.5)
            st.plotly_chart(fig, use_container_width=True)

    # rey was here

    elif page == "Conclusion":
        st.title("Conclusion")
        st.write("""
       The 2018 Happiness Index dataset has revealed several key insights:

        - **Economic Prosperity Matters**: There's a strong positive correlation between GDP per capita and happiness scores.
        - **Social Fabric is Crucial**: Social support shows a significant positive relationship with happiness.
        - **Health is Wealth**: Healthy life expectancy correlates positively with happiness.
        - **Freedom and Corruption Perception**: Higher perceived freedom and lower perceived corruption are associated with higher happiness scores.

        These findings provide a foundation for further research and policy development aimed at improving quality of life globally.
        """)


if __name__ == "__main__":
    main()
