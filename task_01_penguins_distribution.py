# ==============================================================================
# Task 01: Data Distribution Visualization (Palmer Penguins Edition)
# Description: Interactive dashboard featuring KPI Cards, an Executive Summary, a Box Plot, and a Stacked Histogram using the Palmer Penguins dataset.
# ==============================================================================

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def main():
    print("Fetching Palmer Penguins dataset...")
    # 1. Loading the Dataset
    url = 'https://raw.githubusercontent.com/allisonhorst/palmerpenguins/master/inst/extdata/penguins.csv'
    df = pd.read_csv(url)
    
    # Cleaning data: dropping rows missing our key metrics
    df_clean = df.dropna(subset=['flipper_length_mm', 'species', 'body_mass_g']).copy()
    
    # Calculate KPIs
    total_penguins = len(df_clean)
    avg_mass = df_clean['body_mass_g'].mean()
    avg_flipper = df_clean['flipper_length_mm'].mean()

    print(f"Data loaded successfully. Analyzing {total_penguins} penguin records.\n")
    print("Generating Vibrant Interactive Dashboard...")

    # 2. Creating Advanced Subplots Grid
    #using a 2-row layout. Row 1 is for 3 KPI cards. Row 2 is for the 2 charts.
    # The 'specs' array tells Plotly the "type" of chart going into each slot.
    fig = make_subplots(
        rows=2, cols=6, 
        row_heights=[0.2, 0.8],
        vertical_spacing=0.15,
        horizontal_spacing=0.08,
        specs=[
            [{"type": "indicator", "colspan": 2}, None, {"type": "indicator", "colspan": 2}, None, {"type": "indicator", "colspan": 2}, None],
            [{"type": "xy", "colspan": 3}, None, None, {"type": "xy", "colspan": 3}, None, None]
        ],
        subplot_titles=(
            "", "", "", # No titles for the KPI row
            "<b>Flipper Length by Species (Box Plot)</b>", 
            "<b>Distribution of Flipper Lengths (Histogram)</b>"
        )
    )

    # ==========================================================================
    # ROW 1: KPI CARDS (Indicators)
    # ==========================================================================
    fig.add_trace(go.Indicator(
        mode="number", value=total_penguins, title={"text": "<b>Total Penguins</b>"},
    ), row=1, col=1)

    fig.add_trace(go.Indicator(
        mode="number", value=avg_mass, title={"text": "<b>Avg Body Mass (g)</b>"},
        number={"valueformat": ".0f"}
    ), row=1, col=3)

    fig.add_trace(go.Indicator(
        mode="number", value=avg_flipper, title={"text": "<b>Avg Flipper Length (mm)</b>"},
        number={"valueformat": ".1f"}
    ), row=1, col=5)

    # ==========================================================================
    # ROW 2: CHARTS
    # ==========================================================================
    colors = {'Adelie': '#FF8C00', 'Chinstrap': '#8A2BE2', 'Gentoo': '#058B8C'}
    species_list = ['Adelie', 'Chinstrap', 'Gentoo']

    for sp in species_list:
        sp_data = df_clean[df_clean['species'] == sp]['flipper_length_mm']

        # Box Plot (Row 2, Col 1)
        fig.add_trace(go.Box(
            y=sp_data, name=sp, marker_color=colors[sp],
            boxpoints='all', jitter=0.3, pointpos=-1.8,
            hovertemplate="<b>Species:</b> " + sp + "<br><b>Length:</b> %{y}mm<extra></extra>",
            legendgroup=sp, showlegend=False
        ), row=2, col=1)

        # Histogram (Row 2, Col 4 - because of colspan)
        fig.add_trace(go.Histogram(
            x=sp_data, name=sp, marker_color=colors[sp],
            nbinsx=30, opacity=0.9,
            hovertemplate="<b>Length Range:</b> %{x}mm<br><b>Count:</b> %{y}<extra></extra>",
            marker_line_color='black', marker_line_width=1,
            legendgroup=sp, showlegend=True
        ), row=2, col=4)

    # ==========================================================================
    # FORMATTING &  SUMMARY
    # ==========================================================================
    fig.update_layout(
        title_text="<b>Palmer Penguins Demographics Analysis</b>",
        title_font_size=34, title_x=0.5, title_y=0.95,
        template="plotly_white", barmode='stack',
        legend=dict(title="<b>Species</b>", x=1.02, y=0.5, bgcolor='rgba(255,255,255,0.9)', bordercolor='black', borderwidth=1),
        bargap=0.05, autosize=True, 
        margin=dict(l=80, r=120, t=220, b=80),
        paper_bgcolor='#E8F0FE', plot_bgcolor='white'
    )

    # Adding the  Summary Annotation
    fig.add_annotation(
        text=(
            "<b> Summary:</b> Analysis reveals distinct morphological variations across species. "
            "Gentoo penguins<br>exhibit significantly longer flippers and higher body mass, representing a distinct demographic cohort."
        ),
        xref="paper", yref="paper",
        x=0.5, y=1.25, # Positions it above the charts and KPIs
        showarrow=False,
        font=dict(size=14, color="black"),
        bgcolor="white", bordercolor="black", borderwidth=1, borderpad=10
    )

    #  borders
    fig.update_xaxes(showline=True, linewidth=2, linecolor='black', mirror=True, row=2)
    fig.update_yaxes(showline=True, linewidth=2, linecolor='black', mirror=True, row=2)

    # Axis titles
    fig.update_xaxes(title_text="<b>Species</b>", row=2, col=1)
    fig.update_yaxes(title_text="<b>Flipper Length (mm)</b>", row=2, col=1)
    fig.update_xaxes(title_text="<b>Flipper Length (mm)</b>", row=2, col=4)
    fig.update_yaxes(title_text="<b>Frequency</b>", row=2, col=4)

    # Export and Display
    html_filename = "Task_01_Penguins_Dashboard.html"
    fig.write_html(html_filename)
    print(f"✅ Success! Interactive dashboard saved as '{html_filename}' in your folder.")
    fig.show()

if __name__ == "__main__":
    main()