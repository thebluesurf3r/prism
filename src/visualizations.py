import plotly.express as px
import plotly.graph_objects as go

def plot_avg_salary_by_company(df):
    """
    Plots average salary by company using Plotly bar chart.
    """
    avg_salary_by_company = df.groupby('company_name')['salary_numeric'].mean().reset_index()
    fig = px.bar(
        avg_salary_by_company,
        x='company_name',
        y='salary_numeric',
        title="Average Salary by Company",
        labels={'salary_numeric': 'Average Salary'},
        # color='company_name',
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    fig.update_layout(
        template='plotly_dark',
        coloraxis_showscale=False  # Disable the color scale bar
    )
    return fig

def plot_salary_band_distribution(df):
    """
    Plots salary band distribution using Plotly bar chart.
    """
    salary_band_count = df['salary_band'].value_counts().reset_index()
    salary_band_count.columns = ['salary_band', 'count']
    fig = px.bar(
        salary_band_count,
        x='salary_band',
        y='count',
        color='salary_band',
        title="Salary Band Distribution",
        labels={'count': 'Number of Employees'},
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig.update_layout(
        template='plotly_dark',
        coloraxis_showscale=False  # Disable the color scale bar
    )
    return fig


def plot_parallel_categories(df):
    """
    Plots parallel categories chart to visualize categorical relationships.
    """
    # Ensure relevant columns for the parallel categories plot
    categories = [
                            # 'company_name',
                            'salary_band',
                            'location',
                            'job_title',
                            'job_seniority'
                  ]

    # Filter the dataframe to include only relevant columns
    filtered_df = df[categories + ['salary_numeric']]  # Add salary_numeric for coloring

    # Create the parallel categories chart
    fig = px.parallel_categories(
        filtered_df,
        dimensions=categories,
        color="salary_numeric",  # Use a continuous variable for color
        color_continuous_scale=px.colors.sequential.Magma,  # Set the color scale
        title="Categorical Relationships in Job Data"
    )
    fig.update_layout(
        template='plotly_dark',
        coloraxis_showscale=False  # Disable the color scale bar
    )

    return fig

