import streamlit as st
import pandas as pd
from datetime import datetime
from utils.database import query_db
from utils.readiness_utils import calculate_readiness_score, interpret_readiness_score

def check_authentication():
    if "authenticated" not in st.session_state or not st.session_state.authenticated:
        st.warning("Você precisa fazer login para acessar esta página.")
        st.stop()

def save_readiness_assessment(data):
    query = """
    INSERT INTO readiness_assessment 
    (user_id, date, sleep_quality, sleep_duration, stress_level, 
    muscle_soreness, energy_level, motivation, nutrition_quality, 
    hydration, readiness_score, notes)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    try:
        query_db(query, (
            st.session_state.user_id,
            data['date'],
            data['sleep_quality'],
            data['sleep_duration'],
            data['stress_level'],
            data['muscle_soreness'],
            data['energy_level'],
            data['motivation'],
            data['nutrition_quality'],
            data['hydration'],
            data['readiness_score'],
            data['notes']
        ))
        return True
    except Exception as e:
        st.error(f"Erro ao salvar avaliação: {str(e)}")
        return False

def get_user_assessments():
    query = """
    SELECT date, readiness_score, sleep_quality, energy_level, motivation
    FROM readiness_assessment
    WHERE user_id = %s
    ORDER BY date DESC
    LIMIT 10
    """
    return query_db(query, (st.session_state.user_id,))

def prontidao_page():
    check_authentication()
    
    st.image("https://images.pexels.com/photos/864939/pexels-photo-864939.jpeg", use_column_width=True)
    st.title("Módulo de Prontidão")
    
    tab1, tab2, tab3 = st.tabs(["Nova Avaliação", "Histórico", "Análise"])
    
    with tab1:
        st.subheader("Nova Avaliação de Prontidão")
        with st.form("readiness_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                date = st.date_input("Data", datetime.now())
                sleep_quality = st.slider("Qualidade do Sono (1-10)", 1, 10, 5)
                sleep_duration = st.number_input("Duração do Sono (horas)", 0, 24, 8)
                stress_level = st.slider("Nível de Estresse (1-10)", 1, 10, 5)
                muscle_soreness = st.slider("Dor Muscular (1-10)", 1, 10, 5)
            
            with col2:
                energy_level = st.slider("Nível de Energia (1-10)", 1, 10, 5)
                motivation = st.slider("Motivação (1-10)", 1, 10, 5)
                nutrition_quality = st.slider("Qualidade da Nutrição (1-10)", 1, 10, 5)
                hydration = st.slider("Hidratação (1-10)", 1, 10, 5)
            
            notes = st.text_area("Observações")
            submit = st.form_submit_button("Salvar Avaliação")
            
            if submit:
                data = {
                    'date': date,
                    'sleep_quality': sleep_quality,
                    'sleep_duration': sleep_duration,
                    'stress_level': stress_level,
                    'muscle_soreness': muscle_soreness,
                    'energy_level': energy_level,
                    'motivation': motivation,
                    'nutrition_quality': nutrition_quality,
                    'hydration': hydration,
                    'notes': notes
                }
                
                # Calcular score de prontidão
                data['readiness_score'] = calculate_readiness_score(data)
                
                if save_readiness_assessment(data):
                    st.success("Avaliação salva com sucesso!")
                    st.markdown(f"### Score de Prontidão: {data['readiness_score']:.1f}/10")
                    st.info(f"Interpretação: {interpret_readiness_score(data['readiness_score'])}")
    
    with tab2:
        st.subheader("Histórico de Avaliações")
        assessments = get_user_assessments()
        if assessments:
            df = pd.DataFrame(assessments)
            st.line_chart(df.set_index('date')['readiness_score'])
            st.dataframe(df)
        else:
            st.info("Nenhuma avaliação registrada ainda.")
    
    with tab3:
        st.subheader("Análise de Tendências")
        assessments = get_user_assessments()
        if assessments:
            df = pd.DataFrame(assessments)
            
            st.markdown("### Correlações")
            correlation_data = df[['sleep_quality', 'energy_level', 'motivation', 'readiness_score']]
            st.write("Correlação entre diferentes métricas:")
            st.write(correlation_data.corr())
            
            st.markdown("### Médias Semanais")
            df['date'] = pd.to_datetime(df['date'])
            weekly_avg = df.resample('W', on='date')['readiness_score'].mean()
            st.line_chart(weekly_avg)
        else:
            st.info("Dados insuficientes para análise.")

if __name__ == "__main__":
    prontidao_page()
