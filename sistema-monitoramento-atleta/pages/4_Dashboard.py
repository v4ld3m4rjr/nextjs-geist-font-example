import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from utils.database import query_db
from utils.visualization import plot_weekly_metrics

def check_authentication():
    if "authenticated" not in st.session_state or not st.session_state.authenticated:
        st.warning("Você precisa fazer login para acessar esta página.")
        st.stop()

def get_recent_metrics():
    # Últimos 30 dias de dados
    thirty_days_ago = datetime.now() - timedelta(days=30)
    
    readiness_query = """
    SELECT date, readiness_score, sleep_quality, energy_level
    FROM readiness_assessment
    WHERE user_id = %s AND date >= %s
    ORDER BY date DESC
    """
    
    training_query = """
    SELECT date, training_load, rpe, fatigue_level
    FROM training_assessment
    WHERE user_id = %s AND date >= %s
    ORDER BY date DESC
    """
    
    psychological_query = """
    SELECT date, stress_score, anxiety_score, confidence_level, emotional_state
    FROM psychological_assessment
    WHERE user_id = %s AND date >= %s
    ORDER BY date DESC
    """
    
    readiness_data = query_db(readiness_query, (st.session_state.user_id, thirty_days_ago))
    training_data = query_db(training_query, (st.session_state.user_id, thirty_days_ago))
    psychological_data = query_db(psychological_query, (st.session_state.user_id, thirty_days_ago))
    
    return readiness_data, training_data, psychological_data

def calculate_weekly_load(training_data):
    if not training_data:
        return 0
    df = pd.DataFrame(training_data)
    df['date'] = pd.to_datetime(df['date'])
    return df['training_load'].sum()

def dashboard_page():
    check_authentication()
    
    st.image("https://images.pexels.com/photos/1552242/pexels-photo-1552242.jpeg", use_column_width=True)
    st.title("Dashboard")
    
    # Obter dados recentes
    readiness_data, training_data, psychological_data = get_recent_metrics()
    
    # Métricas principais
    st.markdown("## Visão Geral")
    col1, col2, col3, col4 = st.columns(4)
    
    # Última prontidão
    with col1:
        latest_readiness = readiness_data[0] if readiness_data else None
        readiness_score = latest_readiness['readiness_score'] if latest_readiness else "N/A"
        st.metric(
            label="Última Prontidão",
            value=f"{readiness_score}/10" if readiness_score != "N/A" else "N/A"
        )
    
    # Carga semanal
    with col2:
        weekly_load = calculate_weekly_load(training_data)
        st.metric(
            label="Carga Semanal",
            value=f"{weekly_load:.0f} UA"
        )
    
    # Estado psicológico
    with col3:
        latest_psych = psychological_data[0] if psychological_data else None
        emotional_state = latest_psych['emotional_state'] if latest_psych else "N/A"
        st.metric(
            label="Estado Emocional",
            value=f"{emotional_state}/10" if emotional_state != "N/A" else "N/A"
        )
    
    # Nível de fadiga
    with col4:
        latest_training = training_data[0] if training_data else None
        fatigue = latest_training['fatigue_level'] if latest_training else "N/A"
        st.metric(
            label="Nível de Fadiga",
            value=f"{fatigue}/10" if fatigue != "N/A" else "N/A"
        )
    
    # Gráficos de tendências
    st.markdown("## Tendências")
    
    # Prontidão e Carga
    st.markdown("### Prontidão vs Carga de Treino")
    tab1, tab2 = st.tabs(["Últimos 7 dias", "Últimos 30 dias"])
    
    with tab1:
        if readiness_data and training_data:
            df_readiness = pd.DataFrame(readiness_data)
            df_training = pd.DataFrame(training_data)
            
            df_readiness['date'] = pd.to_datetime(df_readiness['date'])
            df_training['date'] = pd.to_datetime(df_training['date'])
            
            # Filtrar últimos 7 dias
            seven_days_ago = datetime.now() - timedelta(days=7)
            df_readiness = df_readiness[df_readiness['date'] >= seven_days_ago]
            df_training = df_training[df_training['date'] >= seven_days_ago]
            
            col1, col2 = st.columns(2)
            with col1:
                st.line_chart(df_readiness.set_index('date')['readiness_score'])
            with col2:
                st.line_chart(df_training.set_index('date')['training_load'])
        else:
            st.info("Dados insuficientes para mostrar tendências dos últimos 7 dias.")
    
    with tab2:
        if readiness_data and training_data:
            df_readiness = pd.DataFrame(readiness_data)
            df_training = pd.DataFrame(training_data)
            
            col1, col2 = st.columns(2)
            with col1:
                st.line_chart(df_readiness.set_index('date')['readiness_score'])
            with col2:
                st.line_chart(df_training.set_index('date')['training_load'])
        else:
            st.info("Dados insuficientes para mostrar tendências dos últimos 30 dias.")
    
    # Estado Psicológico
    st.markdown("### Métricas Psicológicas")
    if psychological_data:
        df_psych = pd.DataFrame(psychological_data)
        df_psych['date'] = pd.to_datetime(df_psych['date'])
        
        metrics = ['stress_score', 'anxiety_score', 'confidence_level', 'emotional_state']
        st.line_chart(df_psych.set_index('date')[metrics])
    else:
        st.info("Dados psicológicos insuficientes para análise.")
    
    # Correlações
    st.markdown("## Análise de Correlações")
    if readiness_data and training_data and psychological_data:
        # Preparar dados
        df_readiness = pd.DataFrame(readiness_data)
        df_training = pd.DataFrame(training_data)
        df_psych = pd.DataFrame(psychological_data)
        
        # Mesclar dataframes na data
        df_readiness['date'] = pd.to_datetime(df_readiness['date'])
        df_training['date'] = pd.to_datetime(df_training['date'])
        df_psych['date'] = pd.to_datetime(df_psych['date'])
        
        df_merged = pd.merge(df_readiness, df_training, on='date', how='outer')
        df_merged = pd.merge(df_merged, df_psych, on='date', how='outer')
        
        # Selecionar métricas principais para correlação
        correlation_metrics = [
            'readiness_score', 'sleep_quality', 'energy_level',
            'training_load', 'fatigue_level',
            'stress_score', 'confidence_level'
        ]
        
        correlation_matrix = df_merged[correlation_metrics].corr()
        
        st.write("Matriz de Correlação entre Métricas Principais:")
        st.write(correlation_matrix)
    else:
        st.info("Dados insuficientes para análise de correlações.")
    
    # Alertas e Recomendações
    st.markdown("## Alertas e Recomendações")
    
    alerts = []
    
    # Verificar prontidão baixa
    if latest_readiness and latest_readiness['readiness_score'] < 5:
        alerts.append("⚠️ Prontidão baixa detectada. Considere reduzir a intensidade do próximo treino.")
    
    # Verificar carga de treino alta
    if weekly_load > 1000:
        alerts.append("⚠️ Carga de treino semanal elevada. Recomenda-se período de recuperação.")
    
    # Verificar estado psicológico
    if latest_psych:
        if latest_psych['stress_score'] > 7:
            alerts.append("⚠️ Nível de estresse elevado. Considere técnicas de relaxamento.")
        if latest_psych['anxiety_score'] > 7:
            alerts.append("⚠️ Nível de ansiedade elevado. Recomenda-se consulta com psicólogo esportivo.")
    
    if alerts:
        for alert in alerts:
            st.warning(alert)
    else:
        st.success("Nenhum alerta importante no momento. Continue com o planejamento normal.")

if __name__ == "__main__":
    dashboard_page()
