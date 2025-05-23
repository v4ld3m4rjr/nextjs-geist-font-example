import streamlit as st
import pandas as pd
from datetime import datetime
from utils.database import query_db
from utils.psychological_utils import calculate_psychological_status

def check_authentication():
    if "authenticated" not in st.session_state or not st.session_state.authenticated:
        st.warning("Você precisa fazer login para acessar esta página.")
        st.stop()

def save_psychological_assessment(data):
    query = """
    INSERT INTO psychological_assessment 
    (user_id, date, depression_score, anxiety_score, stress_score,
    intrinsic_motivation, extrinsic_motivation, amotivation,
    flow_score, confidence_level, focus_ability,
    emotional_state, pre_competition_anxiety,
    satisfaction_with_training, team_cohesion, notes)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    try:
        query_db(query, (
            st.session_state.user_id,
            data['date'],
            data['depression_score'],
            data['anxiety_score'],
            data['stress_score'],
            data['intrinsic_motivation'],
            data['extrinsic_motivation'],
            data['amotivation'],
            data['flow_score'],
            data['confidence_level'],
            data['focus_ability'],
            data['emotional_state'],
            data['pre_competition_anxiety'],
            data['satisfaction_with_training'],
            data['team_cohesion'],
            data['notes']
        ))
        return True
    except Exception as e:
        st.error(f"Erro ao salvar avaliação: {str(e)}")
        return False

def get_user_psychological_history():
    query = """
    SELECT date, depression_score, anxiety_score, stress_score,
           intrinsic_motivation, confidence_level, emotional_state
    FROM psychological_assessment
    WHERE user_id = %s
    ORDER BY date DESC
    LIMIT 10
    """
    return query_db(query, (st.session_state.user_id,))

def psicologico_page():
    check_authentication()
    
    st.image("https://images.pexels.com/photos/3755761/pexels-photo-3755761.jpeg", use_column_width=True)
    st.title("Módulo Psicológico")
    
    tab1, tab2, tab3 = st.tabs(["Nova Avaliação", "Histórico", "Análise"])
    
    with tab1:
        st.subheader("Avaliação Psicológica")
        with st.form("psychological_form"):
            date = st.date_input("Data", datetime.now())
            
            st.markdown("### Estado Emocional e Estresse")
            col1, col2 = st.columns(2)
            with col1:
                depression_score = st.slider("Nível de Depressão (1-10)", 1, 10, 1)
                anxiety_score = st.slider("Nível de Ansiedade (1-10)", 1, 10, 1)
                stress_score = st.slider("Nível de Estresse (1-10)", 1, 10, 1)
            with col2:
                emotional_state = st.slider("Estado Emocional (1-10)", 1, 10, 5)
                pre_competition_anxiety = st.slider("Ansiedade Pré-competição (1-10)", 1, 10, 1)
            
            st.markdown("### Motivação e Foco")
            col3, col4 = st.columns(2)
            with col3:
                intrinsic_motivation = st.slider("Motivação Intrínseca (1-10)", 1, 10, 5)
                extrinsic_motivation = st.slider("Motivação Extrínseca (1-10)", 1, 10, 5)
                amotivation = st.slider("Desmotivação (1-10)", 1, 10, 1)
            with col4:
                flow_score = st.slider("Estado de Flow (1-10)", 1, 10, 5)
                focus_ability = st.slider("Capacidade de Foco (1-10)", 1, 10, 5)
            
            st.markdown("### Performance e Equipe")
            col5, col6 = st.columns(2)
            with col5:
                confidence_level = st.slider("Nível de Confiança (1-10)", 1, 10, 5)
                satisfaction_with_training = st.slider("Satisfação com Treinos (1-10)", 1, 10, 5)
            with col6:
                team_cohesion = st.slider("Coesão com a Equipe (1-10)", 1, 10, 5)
            
            notes = st.text_area("Observações Adicionais")
            submit = st.form_submit_button("Salvar Avaliação")
            
            if submit:
                data = {
                    'date': date,
                    'depression_score': depression_score,
                    'anxiety_score': anxiety_score,
                    'stress_score': stress_score,
                    'intrinsic_motivation': intrinsic_motivation,
                    'extrinsic_motivation': extrinsic_motivation,
                    'amotivation': amotivation,
                    'flow_score': flow_score,
                    'confidence_level': confidence_level,
                    'focus_ability': focus_ability,
                    'emotional_state': emotional_state,
                    'pre_competition_anxiety': pre_competition_anxiety,
                    'satisfaction_with_training': satisfaction_with_training,
                    'team_cohesion': team_cohesion,
                    'notes': notes
                }
                
                if save_psychological_assessment(data):
                    st.success("Avaliação psicológica salva com sucesso!")
                    
                    # Calcular e mostrar status psicológico geral
                    status = calculate_psychological_status(data)
                    st.markdown(f"### Status Psicológico Geral: {status}")
                    
                    # Alertas baseados nos scores
                    if stress_score > 7 or anxiety_score > 7 or depression_score > 7:
                        st.warning("Níveis elevados de estresse/ansiedade/depressão detectados. Considere consultar um profissional.")
    
    with tab2:
        st.subheader("Histórico de Avaliações")
        psychological_history = get_user_psychological_history()
        if psychological_history:
            df = pd.DataFrame(psychological_history)
            
            # Gráfico de tendências emocionais
            st.markdown("### Tendências Emocionais")
            emotional_data = df[['date', 'depression_score', 'anxiety_score', 'stress_score']]
            st.line_chart(emotional_data.set_index('date'))
            
            # Gráfico de motivação
            st.markdown("### Nível de Motivação e Confiança")
            motivation_data = df[['date', 'intrinsic_motivation', 'confidence_level']]
            st.line_chart(motivation_data.set_index('date'))
            
            # Tabela detalhada
            st.markdown("### Registros Detalhados")
            st.dataframe(df)
        else:
            st.info("Nenhuma avaliação psicológica registrada ainda.")
    
    with tab3:
        st.subheader("Análise Psicológica")
        psychological_history = get_user_psychological_history()
        if psychological_history:
            df = pd.DataFrame(psychological_history)
            
            # Correlações entre variáveis
            st.markdown("### Correlações")
            correlation_data = df[[
                'depression_score', 'anxiety_score', 'stress_score',
                'intrinsic_motivation', 'confidence_level', 'emotional_state'
            ]]
            st.write("Correlação entre métricas psicológicas:")
            st.write(correlation_data.corr())
            
            # Médias semanais do estado emocional
            st.markdown("### Médias Semanais - Estado Emocional")
            df['date'] = pd.to_datetime(df['date'])
            weekly_emotional = df.resample('W', on='date')['emotional_state'].mean()
            st.line_chart(weekly_emotional)
            
            # Distribuição dos níveis de estresse
            st.markdown("### Distribuição dos Níveis de Estresse")
            stress_dist = df['stress_score'].value_counts().sort_index()
            st.bar_chart(stress_dist)
        else:
            st.info("Dados insuficientes para análise.")

if __name__ == "__main__":
    psicologico_page()
