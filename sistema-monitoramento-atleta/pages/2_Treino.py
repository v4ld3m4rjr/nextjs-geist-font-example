import streamlit as st
import pandas as pd
from datetime import datetime
from utils.database import query_db
from utils.training_utils import calculate_training_load

def check_authentication():
    if "authenticated" not in st.session_state or not st.session_state.authenticated:
        st.warning("Você precisa fazer login para acessar esta página.")
        st.stop()

def save_training_assessment(data):
    query = """
    INSERT INTO training_assessment 
    (user_id, date, training_load, training_duration, rpe, 
    intensity_zone, training_type, fatigue_level, performance_feeling, notes)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    try:
        query_db(query, (
            st.session_state.user_id,
            data['date'],
            data['training_load'],
            data['training_duration'],
            data['rpe'],
            data['intensity_zone'],
            data['training_type'],
            data['fatigue_level'],
            data['performance_feeling'],
            data['notes']
        ))
        return True
    except Exception as e:
        st.error(f"Erro ao salvar treino: {str(e)}")
        return False

def get_user_training_history():
    query = """
    SELECT date, training_load, training_duration, rpe, training_type, fatigue_level
    FROM training_assessment
    WHERE user_id = %s
    ORDER BY date DESC
    LIMIT 10
    """
    return query_db(query, (st.session_state.user_id,))

def treino_page():
    check_authentication()
    
    st.image("https://images.pexels.com/photos/841130/pexels-photo-841130.jpeg", use_column_width=True)
    st.title("Módulo de Treino")
    
    tab1, tab2, tab3 = st.tabs(["Novo Treino", "Histórico", "Análise"])
    
    with tab1:
        st.subheader("Registro de Treino")
        with st.form("training_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                date = st.date_input("Data", datetime.now())
                training_type = st.selectbox(
                    "Tipo de Treino",
                    ["Força", "Resistência", "Velocidade", "Técnico", "Tático", "Recuperação"]
                )
                training_duration = st.number_input("Duração (minutos)", 0, 480, 60)
                rpe = st.slider("Percepção de Esforço (RPE) (1-10)", 1, 10, 5)
            
            with col2:
                intensity_zone = st.selectbox(
                    "Zona de Intensidade",
                    ["Z1 - Recuperação", "Z2 - Base", "Z3 - Moderado", "Z4 - Limiar", "Z5 - Máximo"]
                )
                fatigue_level = st.slider("Nível de Fadiga (1-10)", 1, 10, 5)
                performance_feeling = st.slider("Sensação de Performance (1-10)", 1, 10, 5)
            
            notes = st.text_area("Observações do Treino")
            submit = st.form_submit_button("Salvar Treino")
            
            if submit:
                # Calcular carga de treino (Training Load)
                training_load = calculate_training_load(training_duration, rpe)
                
                data = {
                    'date': date,
                    'training_type': training_type,
                    'training_duration': training_duration,
                    'rpe': rpe,
                    'intensity_zone': intensity_zone,
                    'fatigue_level': fatigue_level,
                    'performance_feeling': performance_feeling,
                    'training_load': training_load,
                    'notes': notes
                }
                
                if save_training_assessment(data):
                    st.success("Treino registrado com sucesso!")
                    st.markdown(f"### Carga de Treino: {training_load:.1f} UA")
                    
                    if training_load > 500:
                        st.warning("Atenção: Carga de treino elevada. Considere um período adequado de recuperação.")
    
    with tab2:
        st.subheader("Histórico de Treinos")
        training_history = get_user_training_history()
        if training_history:
            df = pd.DataFrame(training_history)
            
            # Gráfico de carga de treino
            st.markdown("### Carga de Treino ao Longo do Tempo")
            st.line_chart(df.set_index('date')['training_load'])
            
            # Distribuição dos tipos de treino
            st.markdown("### Distribuição dos Tipos de Treino")
            training_type_dist = df['training_type'].value_counts()
            st.bar_chart(training_type_dist)
            
            # Tabela detalhada
            st.markdown("### Registros Detalhados")
            st.dataframe(df)
        else:
            st.info("Nenhum treino registrado ainda.")
    
    with tab3:
        st.subheader("Análise de Treinos")
        training_history = get_user_training_history()
        if training_history:
            df = pd.DataFrame(training_history)
            
            # Carga de treino semanal
            st.markdown("### Carga Semanal")
            df['date'] = pd.to_datetime(df['date'])
            weekly_load = df.resample('W', on='date')['training_load'].sum()
            st.line_chart(weekly_load)
            
            # Correlação entre variáveis
            st.markdown("### Correlações")
            correlation_data = df[['training_load', 'rpe', 'fatigue_level', 'performance_feeling']]
            st.write("Correlação entre métricas de treino:")
            st.write(correlation_data.corr())
            
            # Média de RPE por tipo de treino
            st.markdown("### RPE Médio por Tipo de Treino")
            avg_rpe = df.groupby('training_type')['rpe'].mean()
            st.bar_chart(avg_rpe)
        else:
            st.info("Dados insuficientes para análise.")

if __name__ == "__main__":
    treino_page()
