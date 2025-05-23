import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def plot_weekly_metrics(df, date_column, metrics, titles):
    """
    Cria gráficos semanais para as métricas especificadas
    
    Args:
        df: DataFrame com os dados
        date_column: Nome da coluna de data
        metrics: Lista de colunas de métricas para plotar
        titles: Lista de títulos para cada métrica
    """
    df[date_column] = pd.to_datetime(df[date_column])
    weekly_data = df.resample('W', on=date_column)[metrics].mean()
    
    fig = make_subplots(rows=len(metrics), cols=1,
                       subplot_titles=titles,
                       vertical_spacing=0.1)
    
    for i, metric in enumerate(metrics, 1):
        fig.add_trace(
            go.Scatter(x=weekly_data.index, y=weekly_data[metric],
                      mode='lines+markers',
                      name=titles[i-1]),
            row=i, col=1
        )
    
    fig.update_layout(height=300*len(metrics),
                     showlegend=False,
                     title_text="Métricas Semanais")
    
    return fig

def create_correlation_heatmap(df, columns, labels):
    """
    Cria um mapa de calor de correlação entre as métricas
    
    Args:
        df: DataFrame com os dados
        columns: Lista de colunas para correlação
        labels: Lista de rótulos para as colunas
    """
    corr_matrix = df[columns].corr()
    
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix,
        x=labels,
        y=labels,
        colorscale='RdBu',
        zmin=-1, zmax=1
    ))
    
    fig.update_layout(
        title='Matriz de Correlação',
        xaxis_title='Métricas',
        yaxis_title='Métricas'
    )
    
    return fig

def plot_training_distribution(df, type_column='training_type'):
    """
    Cria um gráfico de pizza com a distribuição dos tipos de treino
    
    Args:
        df: DataFrame com os dados
        type_column: Nome da coluna com os tipos de treino
    """
    training_dist = df[type_column].value_counts()
    
    fig = go.Figure(data=[go.Pie(
        labels=training_dist.index,
        values=training_dist.values,
        hole=.3
    )])
    
    fig.update_layout(
        title='Distribuição dos Tipos de Treino'
    )
    
    return fig

def plot_readiness_components(df):
    """
    Cria um gráfico de radar com os componentes da prontidão
    
    Args:
        df: DataFrame com os dados mais recentes de prontidão
    """
    components = [
        'sleep_quality', 'sleep_duration', 'stress_level',
        'muscle_soreness', 'energy_level', 'motivation',
        'nutrition_quality', 'hydration'
    ]
    
    values = [df[comp].iloc[-1] for comp in components]
    
    fig = go.Figure(data=go.Scatterpolar(
        r=values,
        theta=components,
        fill='toself'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10]
            )
        ),
        showlegend=False,
        title='Componentes da Prontidão'
    )
    
    return fig

def plot_psychological_profile(df):
    """
    Cria um gráfico de radar com o perfil psicológico
    
    Args:
        df: DataFrame com os dados psicológicos mais recentes
    """
    components = [
        'confidence_level', 'focus_ability', 'emotional_state',
        'intrinsic_motivation', 'flow_score', 'team_cohesion'
    ]
    
    values = [df[comp].iloc[-1] for comp in components]
    
    fig = go.Figure(data=go.Scatterpolar(
        r=values,
        theta=components,
        fill='toself'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10]
            )
        ),
        showlegend=False,
        title='Perfil Psicológico'
    )
    
    return fig

def plot_training_load_trend(df, date_column='date', load_column='training_load'):
    """
    Cria um gráfico de linha com a tendência da carga de treino
    
    Args:
        df: DataFrame com os dados de treino
        date_column: Nome da coluna de data
        load_column: Nome da coluna de carga
    """
    df[date_column] = pd.to_datetime(df[date_column])
    
    fig = go.Figure()
    
    # Linha principal de carga
    fig.add_trace(go.Scatter(
        x=df[date_column],
        y=df[load_column],
        mode='lines+markers',
        name='Carga de Treino'
    ))
    
    # Média móvel de 7 dias
    rolling_mean = df[load_column].rolling(window=7).mean()
    fig.add_trace(go.Scatter(
        x=df[date_column],
        y=rolling_mean,
        mode='lines',
        name='Média Móvel (7 dias)',
        line=dict(dash='dash')
    ))
    
    fig.update_layout(
        title='Tendência da Carga de Treino',
        xaxis_title='Data',
        yaxis_title='Carga (UA)'
    )
    
    return fig
