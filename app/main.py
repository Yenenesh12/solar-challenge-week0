import sys
import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime
current_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(current_dir, '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

from app.utils import load_data
st.set_page_config(
    layout='wide',
    page_title='Solar Farm Analytics',
    page_icon='☀️'
)

st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 700;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2e86ab;
        border-bottom: 2px solid #ff7f0e;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stButton button {
        background: linear-gradient(45deg, #FF6B6B, #FF8E53);
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        border-radius: 25px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
    }
    .info-box {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #ff7f0e;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">☀️ Solar Farm Analytics Dashboard</h1>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 🎛️ Configuration Panel")
    st.markdown("---")
    
    countries = ['Benin', 'Sierra Leone', 'Togo']
    sel_countries = st.multiselect(
        '**Select Countries**',
        countries,
        default=countries,
        help="Choose countries to compare solar data"
    )
    
    metric_info = {
        'GHI': 'Global Horizontal Irradiance',
        'DNI': 'Direct Normal Irradiance',
        'DHI': 'Diffuse Horizontal Irradiance',
        'Tamb': 'Ambient Temperature'
    }
    
    metric = st.selectbox(
        '**Performance Metric**',
        options=list(metric_info.keys()),
        format_func=lambda x: f"{x} - {metric_info[x]}",
        help="Select the solar performance metric to analyze"
    )
    st.markdown("---")
    st.markdown("### 📊 Display Options")
    show_summary = st.checkbox("Show Summary Statistics", value=True)
    show_hourly = st.checkbox("Show Hourly Profile", value=True)
    
    with st.expander("ℹ️ About this Dashboard"):
        st.markdown("""
        This dashboard provides comparative analysis of solar farm performance across 3 countries(Benin, Sierra leon and Togo ).
        
        **Metrics Explained:**
        - **GHI**: Total solar radiation received on a horizontal surface
        - **DNI**: Direct beam radiation from the sun
        - **DHI**: Diffused solar radiation
        - **Tamb**: Ambient air temperature
        """)

st.markdown("### 📥 Data Loading")
load_col1, load_col2 = st.columns([3, 1])

with load_col1:
    st.markdown(f"**Selected Countries:** {', '.join(sel_countries) if sel_countries else 'None'}")
    st.markdown(f"**Selected Metric:** {metric} - {metric_info[metric]}")

with load_col2:
    load_clicked = st.button('🚀 Load & Analyze Data', use_container_width=True)

@st.cache_data
def get_dfs(selected_countries):
    """Loads and caches data to prevent reloading on every Streamlit rerun."""
    dfs = {}
    for c in selected_countries:
        try:
            dfs[c] = load_data(c)
        except (FileNotFoundError, ValueError) as e:
            st.error(f"Failed to load data for {c}: {e}")
            continue
    return dfs

if load_clicked:
    if not sel_countries:
        st.warning("⚠️ Please select at least one country to analyze.")
    else:
        with st.spinner('🔄 Loading solar data...'):
            dfs = get_dfs(sel_countries)
        
        if not dfs:
            st.error("❌ No data was successfully loaded for the selected countries.")
        else:
            if show_summary:
                st.markdown('<div class="sub-header">📈 Performance Summary</div>', unsafe_allow_html=True)
                
                cols = st.columns(len(dfs))
                summary_data = []
                
                for (country, df), col in zip(dfs.items(), cols):
                    with col:
                        if metric in df.columns:
                            mean_val = df[metric].mean()
                            median_val = df[metric].median()
                            std_val = df[metric].std()
                            
                            st.markdown(f"""
                            <div class="metric-card">
                                <h3>{country}</h3>
                                <p><strong>Mean:</strong> {mean_val:.2f}</p>
                                <p><strong>Median:</strong> {median_val:.2f}</p>
                                <p><strong>Std Dev:</strong> {std_val:.2f}</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            summary_data.append({
                                'Country': country,
                                'Mean': mean_val,
                                'Median': median_val,
                                'Std Dev': std_val,
                                'Min': df[metric].min(),
                                'Max': df[metric].max()
                            })
                
                if summary_data:
                    st.markdown("#### Detailed Statistics")
                    summary_df = pd.DataFrame(summary_data).set_index('Country')
                    st.dataframe(summary_df.style.format("{:.2f}").background_gradient(cmap='YlOrBr'), use_container_width=True)
            
            viz_col1, viz_col2 = st.columns([2, 1])
            
            with viz_col1:
                st.markdown('<div class="sub-header">📊 Distribution Analysis</div>', unsafe_allow_html=True)
                
                fig, ax = plt.subplots(figsize=(10, 6))
                data = []
                labels = []
                
                for c, d in dfs.items():
                    if metric in d.columns:
                        data.append(d[metric].dropna())
                        labels.append(c)
                
                if data:
                    box_plot = ax.boxplot(data, labels=labels, patch_artist=True,
                                        showmeans=True, meanline=True,
                                        boxprops=dict(facecolor='lightblue', alpha=0.7),
                                        medianprops=dict(color='red', linewidth=2),
                                        meanprops=dict(color='green', linewidth=2))
                    
                    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
                    for patch, color in zip(box_plot['boxes'], colors):
                        patch.set_facecolor(color)
                    
                    ax.set_title(f'{metric} Distribution by Country\n({metric_info[metric]})',
                               fontsize=14, fontweight='bold', pad=20)
                    ax.set_ylabel(metric, fontweight='bold')
                    ax.grid(axis='y', alpha=0.3, linestyle='--')
                    ax.set_facecolor('#f8f9fa')
                    
                    from matplotlib.lines import Line2D
                    legend_elements = [
                        Line2D([0], [0], color='red', lw=2, label='Median'),
                        Line2D([0], [0], color='green', lw=2, label='Mean')
                    ]
                    ax.legend(handles=legend_elements, loc='upper right')
                    
                    st.pyplot(fig)
                else:
                    st.warning(f"Metric '{metric}' not found in any loaded dataset.")
            
            with viz_col2:
                st.markdown('<div class="sub-header">📋 Data Overview</div>', unsafe_allow_html=True)
                
                st.markdown("#### 📏 Data Quality")
                quality_data = []
                for c, d in dfs.items():
                    total_rows = len(d)
                    missing_metric = d[metric].isna().sum() if metric in d.columns else total_rows
                    quality_data.append({
                        'Country': c,
                        'Total Records': total_rows,
                        'Missing Values': missing_metric,
                        'Data Completeness': f"{((total_rows - missing_metric) / total_rows * 100):.1f}%"
                    })
                
                quality_df = pd.DataFrame(quality_data).set_index('Country')
                st.dataframe(quality_df, use_container_width=True)
                
                st.markdown("#### 💡 Quick Insights")
                if summary_data:
                    best_country = max(summary_data, key=lambda x: x['Mean'])
                    most_consistent = min(summary_data, key=lambda x: x['Std Dev'])
                    
                    st.markdown(f"""
                    <div class="info-box">
                        <strong>Highest Average:</strong> {best_country['Country']} ({best_country['Mean']:.2f})<br>
                        <strong>Most Consistent:</strong> {most_consistent['Country']} (std: {most_consistent['Std Dev']:.2f})
                    </div>
                    """, unsafe_allow_html=True)
            
            if show_hourly:
                st.markdown('<div class="sub-header">🕒 Hourly Profile Comparison</div>', unsafe_allow_html=True)
                
                fig2, ax2 = plt.subplots(figsize=(12, 6))
                has_data = False
                
                colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
                
                for i, (c, d) in enumerate(dfs.items()):
                    if metric in d.columns:
                        d['hour'] = d['Timestamp'].dt.hour
                        hourly = d.groupby('hour')[metric].mean()
                        ax2.plot(hourly.index, hourly.values,
                                marker='o',
                                linewidth=2.5,
                                markersize=6,
                                label=c,
                                color=colors[i % len(colors)],
                                alpha=0.8)
                        has_data = True
                
                if has_data:
                    ax2.set_xlabel('Hour of Day', fontweight='bold', fontsize=12)
                    ax2.set_ylabel(metric, fontweight='bold', fontsize=12)
                    ax2.set_xticks(np.arange(0, 24, 2))
                    ax2.grid(True, alpha=0.3, linestyle='--')
                    ax2.set_facecolor('#f8f9fa')
                    ax2.legend(title='Country', title_fontsize=12, fontsize=10)
                    ax2.set_title(f'Hourly {metric} Profile\n({metric_info[metric]})',
                                fontsize=14, fontweight='bold', pad=20)
                    
                    ax2.spines['top'].set_visible(False)
                    ax2.spines['right'].set_visible(False)
                    
                    st.pyplot(fig2)
                    
                    st.markdown("#### 📈 Peak Performance Analysis")
                    peak_data = []
                    for c, d in dfs.items():
                        if metric in d.columns:
                            d['hour'] = d['Timestamp'].dt.hour
                            hourly = d.groupby('hour')[metric].mean()
                            peak_hour = hourly.idxmax()
                            peak_value = hourly.max()
                            peak_data.append({
                                'Country': c,
                                'Peak Hour': f"{peak_hour:02d}:00",
                                'Peak Value': f"{peak_value:.2f}"
                            })
                    
                    if peak_data:
                        peak_df = pd.DataFrame(peak_data).set_index('Country')
                        st.dataframe(peak_df, use_container_width=True)
                else:
                    st.warning("Could not generate hourly profile as metric was unavailable in the loaded data.")

st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "Solar Farm Analytics Dashboard • Built with Derese Ewunet • "
    f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    "</div>",
    unsafe_allow_html=True
)