import plotly.express as px
import plotly.graph_objects as go

def plot_avg_salary_by_company(df):
    """
    Plots average salary by company using Plotly bar chart.
    """
    avg_salary_by_company = df.groupby('company_name')['salary_numeric'].mean().reset_index()
    fig = px.bar(avg_salary_by_company, x='company_name', y='salary_numeric',
                 title="Average Salary by Company", labels={'salary_numeric': 'Average Salary'})
    fig.update_layout(template='plotly_dark')
    return fig

def plot_salary_band_distribution(df):
    """
    Plots salary band distribution using Plotly bar chart.
    """
    salary_band_count = df['salary_band'].value_counts().reset_index()
    salary_band_count.columns = ['salary_band', 'count']
    fig = px.bar(salary_band_count, x='salary_band', y='count',
                 title="Salary Band Distribution", labels={'count': 'Number of Employees'})
    fig.update_layout(template='plotly_dark')
    return fig
