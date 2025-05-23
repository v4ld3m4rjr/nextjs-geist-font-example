import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from utils.database import query_db
from utils.export import export_to_excel, export_to_pdf
from utils.visualization import plot_weekly_metrics

def check_authentication():
    if "authenticated" not in st.session_state or not st.session_state.authenticated:
        st.warning("Você precisa fazer login para acessar esta página.")
        st.stop()

def get_data_by_date_range(start_date, end_date):
    readiness_query = """
    SELECT date, readiness_score, sleep_quality, sleep_duration, 
           stress_level, muscle_soreness, energy_level, motivation,
           nutrition_quality, hydration, notes
    FROM readiness_assessment
    WHERE user_id = %s AND date BETWEEN %s AND %s
    ORDER BY date
    """
    
    training_query = """
    SELECT date, training_load, training_duration, rpe, 
           intensity_zone, training_type, fatigue_level,
           performance_feeling, notes
    FROM training_assessment
    WHERE user_id = %s AND date BETWEEN %s AND %s
    ORDER BY date
    """
    
    psychological_query = """
    SELECT date, depression_score, anxiety_score, stress_score,
           intrinsic_motivation, extrinsic_motivation, amotivation,
           flow_score, confidence_level, focus_ability,
           emotional_state, pre_competition_anxiety,
           satisfaction_with_training, team_cohesion, notes
    FROM psychological_assessment
    WHERE user_id = %s AND date BETWEEN %s AND %s
    ORDER BY date
    """
    
    readiness_data = query_db(readiness_query, (st.session_state.user_id, start_date, end_date))
    training_data = query_db(training_query, (st.session_state.user_id, start_date, end_date))
    psychological_data = query_db(psychological_query, (st.session_state.user_id, start_date, end_date))
    
    return readiness_data, training_data, psychological_data

def calculate_summary_metrics(readiness_data, training_data, psychological_data):
    summary = {}
    
    if readiness_data:
        df_readiness = pd.DataFrame(readiness_data)
        summary['média_prontidão'] = df_readiness['readiness_score'].mean()
        summary['média_sono'] = df_readiness['sleep_quality'].mean()
        summary['média_energia'] = df_readiness['energy_level'].mean()
    
    if training_data:
        df_training = pd.DataFrame(training_data)
        summary['carga_total'] = df_training['training_load'].sum()
        summary['média_rpe'] = df_training['rpe'].mean()
        summary['total_minutos'] = df_training['training_duration'].sum()
    
    if psychological_data:
        df_psych = pd.DataFrame(psychological_data)
        summary['média_estresse'] = df_psych['stress_score'].mean()
        summary['média_motivação'] = df_psych['intrinsic_motivation'].mean()
        summary['média_confiança'] = df_psych['confidence_level'].mean()
    
    return summary

def relatorios_page():
    check_authentication()
    
    st.image("https://images.pexels.com/photos/669577/pexels-photo-669577.jpeg", use_column_width=True)
    st.title("Relatórios e Análises")
    
    # Seleção de período
    st.markdown("## Selecione o Período")
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Data Inicial", datetime.now() - timedelta(days=30))
    with col2:
        end_date = st.date_input("Data Final", datetime.now())
    
    if start_date > end_date:
        st.error("Data inicial deve ser anterior à data final")
        st.stop()
    
    # Buscar dados
    readiness_data, training_data, psychological_data = get_data_by_date_range(start_date, end_date)
    
    # Métricas resumidas
    st.markdown("## Resumo do Período")
    summary = calculate_summary_metrics(readiness_data, training_data, psychological_data)
    
    if summary:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if 'média_prontidão' in summary:
                st.metric("Média de Prontidão", f"{summary['média_prontidão']:.1f}/10")
            if 'carga_total' in summary:
                st.metric("Carga Total", f"{summary['carga_total']:.0f} UA")
        
        with col2:
            if 'média_sono' in summary:
                st.metric("Média Qualidade Sono", f"{summary['média_sono']:.1f}/10")
            if 'total_minutos' in summary:
                st.metric("Total de Minutos", f"{summary['total_minutos']:.0f}")
        
        with col3:
            if 'média_estresse' in summary:
                st.metric("Média de Estresse", f"{summary['média_estresse']:.1f}/10")
            if 'média_motivação' in summary:
                st.metric("Média Motivação", f"{summary['média_motivação']:.1f}/10")
    
    # Visualizações
    st.markdown("## Visualizações")
    
    tab1, tab2, tab3 = st.tabs(["Prontidão", "Treino", "Psicológico"])
    
    with tab1:
        if readiness_data:
            df_readiness = pd.DataFrame(readiness_data)
            df_readiness['date'] = pd.to_datetime(df_readiness['date'])
            
            st.markdown("### Tendências de Prontidão")
            st.line_chart(df_readiness.set_index('date')['readiness_score'])
            
            st.markdown("### Componentes da Prontidão")
            components = ['sleep_quality', 'energy_level', 'motivation']
            st.line_chart(df_readiness.set_index('date')[components])
        else:
            st.info("Sem dados de prontidão para o período selecionado.")
    
    with tab2:
        if training_data:
            df_training = pd.DataFrame(training_data)
            df_training['date'] = pd.to_datetime(df_training['date'])
            
            st.markdown("### Carga de Treino")
            st.line_chart(df_training.set_index('date')['training_load'])
            
            st.markdown("### Distribuição por Tipo de Treino")
            training_dist = df_training['training_type'].value_counts()
            st.bar_chart(training_dist)
        else:
            st.info("Sem dados de treino para o período selecionado.")
    
    with tab3:
        if psychological_data:
            df_psych = pd.DataFrame(psychological_data)
            df_psych['date'] = pd.to_datetime(df_psych['date'])
            
            st.markdown("### Indicadores Psicológicos")
            indicators = ['stress_score', 'anxiety_score', 'confidence_level']
            st.line_chart(df_psych.set_index('date')[indicators])
            
            st.markdown("### Motivação ao Longo do Tempo")
            motivation = ['intrinsic_motivation', 'extrinsic_motivation', 'amotivation']
            st.line_chart(df_psych.set_index('date')[motivation])
        else:
            st.info("Sem dados psicológicos para o período selecionado.")
    
    # Exportação
    st.markdown("## Exportar Dados")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Exportar para Excel"):
            try:
                excel_file = export_to_excel(readiness_data, training_data, psychological_data)
                st.download_button(
                    label="Baixar Excel",
                    data=excel_file,
                    file_name=f"relatorio_{start_date}_{end_date}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            except Exception as e:
                st.error(f"Erro ao exportar para Excel: {str(e)}")
    
    with col2:
        if st.button("Exportar para PDF"):
            try:
                pdf_file = export_to_pdf(readiness_data, training_data, psychological_data, summary)
                st.download_button(
                    label="Baixar PDF",
                    data=pdf_file,
                    file_name=f"relatorio_{start_date}_{end_date}.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"Erro ao exportar para PDF: {str(e)}")
    
    # Análises Avançadas
    st.markdown("## Análises Avançadas")
    
    if readiness_data and training_data and psychological_data:
        # Converter para DataFrames
        df_readiness = pd.DataFrame(readiness_data)
        df_training = pd.DataFrame(training_data)
        df_psych = pd.DataFrame(psychological_data)
        
        # Correlações
        st.markdown("### Matriz de Correlação")
        metrics = {
            'Prontidão': df_readiness['readiness_score'],
            'Carga de Treino': df_training['training_load'],
            'Estresse': df_psych['stress_score'],
            'Motivação': df_psych['intrinsic_motivation'],
            'Confiança': df_psych['confidence_level']
        }
        
        correlation_df = pd.DataFrame(metrics)
        st.write(correlation_df.corr())
        
        # Tendências semanais
        st.markdown("### Tendências Semanais")
        df_readiness['date'] = pd.to_datetime(df_readiness['date'])
        weekly_readiness = df_readiness.resample('W', on='date')['readiness_score'].mean()
        
        df_training['date'] = pd.to_datetime(df_training['date'])
        weekly_load = df_training.resample('W', on='date')['training_load'].sum()
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Prontidão Média Semanal")
            st.line_chart(weekly_readiness)
        with col2:
            st.markdown("#### Carga Semanal")
            st.line_chart(weekly_load)
    else:
        st.info("Dados insuficientes para análises avançadas.")

if __name__ == "__main__":
    relatorios_page()
