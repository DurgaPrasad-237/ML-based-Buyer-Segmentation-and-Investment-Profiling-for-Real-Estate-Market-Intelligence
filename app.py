import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# ── PAGE CONFIG ───────────────────────────────────────────────
st.set_page_config(
    page_title="Real Estate Buyer Intelligence",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CUSTOM CSS FOR STORYTELLING DESIGN ────────────────────────
st.markdown("""
<style>
    * {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    .header-section {
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        color: white;
        padding: 40px 20px;
        border-radius: 12px;
        margin-bottom: 30px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    .header-section h1 {
        font-size: 2.5em;
        margin: 0;
        font-weight: 700;
        letter-spacing: -1px;
    }
    
    .header-section p {
        font-size: 1.1em;
        margin: 10px 0 0 0;
        opacity: 0.95;
    }
    
    .segment-card {
        background: white;
        padding: 25px;
        border-radius: 12px;
        border-left: 5px solid #3498db;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        margin-bottom: 20px;
        transition: all 0.3s ease;
    }
    
    .segment-card:hover {
        box-shadow: 0 8px 25px rgba(0,0,0,0.12);
        transform: translateY(-2px);
    }
    
    .segment-card.c1 { border-left-color: #3498db; }
    .segment-card.c2 { border-left-color: #e74c3c; }
    .segment-card.c3 { border-left-color: #f39c12; }
    .segment-card.c4 { border-left-color: #2ecc71; }
    
    .metric-row {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 15px;
        margin-top: 15px;
    }
    
    .metric-box {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 15px;
        border-radius: 8px;
        text-align: center;
    }
    
    .metric-value {
        font-size: 1.8em;
        font-weight: 700;
        color: #2c3e50;
    }
    
    .metric-label {
        font-size: 0.85em;
        color: #7f8c8d;
        margin-top: 5px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .insight-box {
        background: #ecf0f1;
        padding: 20px;
        border-radius: 8px;
        border-left: 4px solid #3498db;
        margin: 15px 0;
    }
    
    .insight-title {
        font-weight: 700;
        color: #2c3e50;
        margin-bottom: 8px;
    }
    
    .insight-text {
        color: #34495e;
        line-height: 1.6;
    }
    
    .stTabs [data-baseweb="tab-list"] button {
        font-size: 1.1em;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ── LOAD DATA ─────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv('final_df_with_segments.csv')
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("Error: 'final_df_with_segments.csv' not found. Please ensure the file is in the same directory as app.py")
    st.stop()

# ── SEGMENT MAPPING ───────────────────────────────────────────
segment_names = {
    'C4 - Luxury Investors': 'Luxury Investors',
    'C2 - First-Time Buyers': 'First-Time Buyers',
    'C1 - Global Investors': 'Global Investors',
    'C3 - Corporate Buyers': 'Corporate Buyers'
}

segment_descriptions = {
    'C4 - Luxury Investors': 'Established investors with high satisfaction, large portfolios & premium properties',
    'C2 - First-Time Buyers': 'New buyers seeking financing, building their first portfolio',
    'C1 - Global Investors': 'Satisfied investors with steady growth, diversified holdings',
    'C3 - Corporate Buyers': 'Organizations making strategic acquisitions with high unit prices'
}

# ── HEADER ────────────────────────────────────────────────────
st.markdown("""
<div class="header-section">
    <h1>Real Estate Buyer Intelligence Platform</h1>
    <p>Understand your market through buyer behavior segmentation</p>
</div>
""", unsafe_allow_html=True)

# ── SIDEBAR FILTERS ───────────────────────────────────────────
st.sidebar.markdown("### Filter Options")

selected_countries = st.sidebar.multiselect(
    "Select Country",
    options=sorted(df['country'].unique()),
    default=sorted(df['country'].unique())
)

selected_regions = st.sidebar.multiselect(
    "Select Region",
    options=sorted(df['region'].unique()),
    default=sorted(df['region'].unique())
)

selected_purpose = st.sidebar.multiselect(
    "Acquisition Purpose",
    options=sorted(df['acquisition_purpose'].unique()),
    default=sorted(df['acquisition_purpose'].unique())
)

selected_client_type = st.sidebar.multiselect(
    "Client Type",
    options=sorted(df['client_type'].unique()),
    default=sorted(df['client_type'].unique())
)

# ── APPLY FILTERS ─────────────────────────────────────────────
filtered_df = df[
    (df['country'].isin(selected_countries)) &
    (df['region'].isin(selected_regions)) &
    (df['acquisition_purpose'].isin(selected_purpose)) &
    (df['client_type'].isin(selected_client_type))
]

st.sidebar.markdown(f"### 📊 Data Summary\n**Total Buyers:** {len(filtered_df)}")

# ── ERROR HANDLING: Check if filtered_df is empty ────────────
if len(filtered_df) == 0:
    st.error("No data to display! Please adjust your filters to include at least one buyer.")
    st.stop()

# ── MAIN TABS ─────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "Overview",
    "Investor Behavior",
    "Geographic Analysis",
    "Segment Details"
])

# ═════════════════════════════════════════════════════════════
# TAB 1 — OVERVIEW
# ═════════════════════════════════════════════════════════════
with tab1:
    st.markdown("## Market Snapshot")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_buyers = len(filtered_df)
        st.metric("Total Buyers", f"{total_buyers:,}", delta=None)
    
    with col2:
        avg_investment = filtered_df['total_investment'].mean()
        st.metric("Avg Investment", f"${avg_investment:,.0f}", delta=None)
    
    with col3:
        investment_pct = (filtered_df['acquisition_purpose'].str.lower() == 'investment').sum() / len(filtered_df) * 100
        st.metric("Investment Purpose", f"{investment_pct:.1f}%", delta=None)
    
    with col4:
        avg_satisfaction = filtered_df['satisfaction_score'].mean()
        st.metric("Avg Satisfaction", f"{avg_satisfaction:.2f}/10", delta=None)
    
    st.markdown("---")
    
    # Cluster Distribution Pie Chart
    st.markdown("### Buyer Segment Distribution")
    
    segment_counts = filtered_df['buyer_segment'].value_counts()
    segment_labels = [segment_names.get(seg, seg) for seg in segment_counts.index]
    
    # Map segment colors properly
    segment_colors = {
        'C1 - Global Investors': '#3498db',
        'C2 - First-Time Buyers': '#e74c3c',
        'C3 - Corporate Buyers': '#f39c12',
        'C4 - Luxury Investors': '#2ecc71'
    }
    
    colors = [segment_colors.get(seg, '#95a5a6') for seg in segment_counts.index]
    
    fig_pie = go.Figure(data=[go.Pie(
        labels=segment_labels,
        values=segment_counts.values,
        marker=dict(colors=colors),
        textposition='auto',
        hovertemplate='<b>%{label}</b><br>Buyers: %{value}<br>%{percent}<extra></extra>'
    )])
    
    fig_pie.update_layout(
        height=450,
        showlegend=True,
        font=dict(size=12)
    )
    
    st.plotly_chart(fig_pie, use_container_width=True)
    
    # Key Insights
    st.markdown("###Key Insights")
    
    largest_segment = segment_counts.idxmax()
    largest_count = segment_counts.max()
    largest_pct = (largest_count / len(filtered_df)) * 100
    
    st.markdown(f"""
    <div class="insight-box">
        <div class="insight-title">Largest Segment</div>
        <div class="insight-text">
            {segment_names.get(largest_segment, largest_segment)} represents <b>{largest_pct:.1f}%</b> of the market 
            with <b>{largest_count:,}</b> buyers. {segment_descriptions.get(largest_segment, '')}
        </div>
    </div>
    """, unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════
# TAB 2 — INVESTOR BEHAVIOR
# ═════════════════════════════════════════════════════════════
with tab2:
    st.markdown("## Investor Behavior Patterns")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Investment Purpose by Segment
        st.markdown("### Investment vs Personal Use")
        
        purpose_data = filtered_df.groupby('buyer_segment')['acquisition_purpose'].value_counts().unstack(fill_value=0)
        purpose_pct = purpose_data.div(purpose_data.sum(axis=1), axis=0) * 100
        
        fig_purpose = go.Figure()
        
        for col in purpose_pct.columns:
            fig_purpose.add_trace(go.Bar(
                name=col.title(),
                x=[segment_names.get(seg, seg) for seg in purpose_pct.index],
                y=purpose_pct[col],
                marker=dict(color='#3498db' if col.lower() == 'investment' else '#95a5a6')
            ))
        
        fig_purpose.update_layout(
            barmode='stack',
            height=400,
            xaxis_title="Buyer Segment",
            yaxis_title="Percentage (%)",
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_purpose, use_container_width=True)
    
    with col2:
        # Loan Behavior
        st.markdown("### Financing Needs")
        
        loan_data = filtered_df.groupby('buyer_segment')['loan_applied'].value_counts().unstack(fill_value=0)
        loan_pct = loan_data.div(loan_data.sum(axis=1), axis=0) * 100
        
        fig_loan = go.Figure()
        
        for col in loan_pct.columns:
            fig_loan.add_trace(go.Bar(
                name=col.title(),
                x=[segment_names.get(seg, seg) for seg in loan_pct.index],
                y=loan_pct[col],
                marker=dict(color='#e74c3c' if col.lower() == 'yes' else '#2ecc71')
            ))
        
        fig_loan.update_layout(
            barmode='stack',
            height=400,
            xaxis_title="Buyer Segment",
            yaxis_title="Percentage (%)",
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_loan, use_container_width=True)
    
    # Financial Metrics Table
    st.markdown("### Financial Profile by Segment")
    
    financial_summary = filtered_df.groupby('buyer_segment').agg({
        'property_count': 'mean',
        'total_investment': 'mean',
        'avg_investment': 'mean',
        'satisfaction_score': 'mean'
    }).round(2)
    
    financial_summary.index = [segment_names.get(seg, seg) for seg in financial_summary.index]
    financial_summary.columns = ['Avg Properties', 'Total Investment', 'Avg Unit Price', 'Satisfaction']
    
    st.dataframe(financial_summary, use_container_width=True)

# ═════════════════════════════════════════════════════════════
# TAB 3 — GEOGRAPHIC ANALYSIS
# ═════════════════════════════════════════════════════════════
with tab3:
    st.markdown("## Geographic Distribution")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Buyers by Region
        st.markdown("### Top Regions")
        
        region_segment = pd.crosstab(filtered_df['region'], filtered_df['buyer_segment'])
        region_segment.columns = [segment_names.get(seg, seg) for seg in region_segment.columns]
        
        fig_region = go.Figure()
        
        for col in region_segment.columns:
            fig_region.add_trace(go.Bar(
                name=col,
                y=region_segment.index,
                x=region_segment[col],
                orientation='h',
                marker=dict(color=['#2ecc71', '#e74c3c', '#3498db', '#f39c12'][list(region_segment.columns).index(col)])
            ))
        
        fig_region.update_layout(
            height=400,
            barmode='stack',
            xaxis_title="Number of Buyers",
            yaxis_title="Region",
            hovermode='y unified'
        )
        
        st.plotly_chart(fig_region, use_container_width=True)
    
    with col2:
        # Buyers by Country
        st.markdown("### Top Countries")
        
        country_segment = pd.crosstab(filtered_df['country'], filtered_df['buyer_segment'])
        country_segment.columns = [segment_names.get(seg, seg) for seg in country_segment.columns]
        
        fig_country = go.Figure()
        
        for col in country_segment.columns:
            fig_country.add_trace(go.Bar(
                name=col,
                y=country_segment.index,
                x=country_segment[col],
                orientation='h',
                marker=dict(color=['#2ecc71', '#e74c3c', '#3498db', '#f39c12'][list(country_segment.columns).index(col)])
            ))
        
        fig_country.update_layout(
            height=400,
            barmode='stack',
            xaxis_title="Number of Buyers",
            yaxis_title="Country",
            hovermode='y unified'
        )
        
        st.plotly_chart(fig_country, use_container_width=True)

# ═════════════════════════════════════════════════════════════
# TAB 4 — SEGMENT DETAILS
# ═════════════════════════════════════════════════════════════
with tab4:
    st.markdown("## Deep Dive: Segment Profiles")
    
    for segment in sorted(filtered_df['buyer_segment'].unique()):
        segment_data = filtered_df[filtered_df['buyer_segment'] == segment]
        segment_display_name = segment_names.get(segment, segment)
        
        st.markdown(f"### {segment_display_name}")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Size", f"{len(segment_data):,}")
        
        with col2:
            st.metric("Avg Age", f"{segment_data['age'].mean():.0f} yrs")
        
        with col3:
            st.metric("Satisfaction", f"{segment_data['satisfaction_score'].mean():.2f}/10")
        
        with col4:
            st.metric("Avg Properties", f"{segment_data['property_count'].mean():.1f}")
        
        with col5:
            st.metric("Avg Investment", f"${segment_data['total_investment'].mean()/1e6:.1f}M")
        
        # Description
        st.markdown(f"**Profile:** {segment_descriptions.get(segment, '')}")
        
        # Characteristics
        col1, col2 = st.columns(2)
        
        with col1:
            investment_pct = (segment_data['acquisition_purpose'].str.lower() == 'investment').sum() / len(segment_data) * 100
            st.markdown(f"💼 **Investment Focus:** {investment_pct:.1f}%")
        
        with col2:
            loan_pct = (segment_data['loan_applied'].str.lower() == 'yes').sum() / len(segment_data) * 100
            st.markdown(f"🏦 **Loan Usage:** {loan_pct:.1f}%")
        
        st.markdown("---")

# ── FOOTER ────────────────────────────────────────────────────
st.markdown("""
---
<div style="text-align: center; color: #7f8c8d; font-size: 0.9em; margin-top: 30px;">
    📊 Real Estate Buyer Segmentation Dashboard | Powered by ML Clustering Analysis
</div>
""", unsafe_allow_html=True)