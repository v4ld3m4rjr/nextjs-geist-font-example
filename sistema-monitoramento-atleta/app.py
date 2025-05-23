import streamlit as st
from utils.auth import register_user, authenticate_user
from utils.database import query_db

def init_session_state():
    if "user_id" not in st.session_state:
        st.session_state.user_id = None
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

def login_form():
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Senha", type="password")
        submit = st.form_submit_button("Entrar")
        
        if submit:
            user_id = authenticate_user(email, password)
            if user_id:
                st.session_state.user_id = user_id
                st.session_state.authenticated = True
                st.success("Login realizado com sucesso!")
                st.experimental_rerun()
            else:
                st.error("Email ou senha incorretos")

def register_form():
    with st.form("register_form"):
        name = st.text_input("Nome")
        email = st.text_input("Email")
        password = st.text_input("Senha", type="password")
        password_confirm = st.text_input("Confirme a Senha", type="password")
        submit = st.form_submit_button("Registrar")
        
        if submit:
            if password != password_confirm:
                st.error("As senhas não coincidem")
                return
            
            try:
                register_user(email, password, name)
                st.success("Registro realizado com sucesso! Faça login para continuar.")
            except Exception as e:
                if "duplicate key" in str(e):
                    st.error("Este email já está registrado")
                else:
                    st.error("Erro ao registrar usuário")

def main():
    st.set_page_config(
        page_title="Sistema de Monitoramento do Atleta",
        page_icon="🏃",
        layout="wide"
    )
    
    init_session_state()
    
    # Cabeçalho com imagem
    st.image("https://images.pexels.com/photos/2294361/pexels-photo-2294361.jpeg", use_column_width=True)
    st.title("Sistema de Monitoramento do Atleta")
    
    if not st.session_state.authenticated:
        st.sidebar.title("Autenticação")
        menu = ["Login", "Registro"]
        choice = st.sidebar.selectbox("Menu", menu)
        
        if choice == "Login":
            st.subheader("Login")
            login_form()
        else:
            st.subheader("Registro")
            register_form()
    else:
        st.sidebar.title(f"Bem-vindo!")
        if st.sidebar.button("Sair"):
            st.session_state.authenticated = False
            st.session_state.user_id = None
            st.experimental_rerun()
        
        st.header("Dashboard Principal")
        
        # Métricas principais
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="Prontidão", value="8.5/10")
        with col2:
            st.metric(label="Carga de Treino", value="320 UA")
        with col3:
            st.metric(label="Estado Psicológico", value="Bom")
        
        # Seção de acesso rápido
        st.subheader("Acesso Rápido")
        quick_access_col1, quick_access_col2 = st.columns(2)
        
        with quick_access_col1:
            st.markdown("### Avaliações")
            st.button("Nova Avaliação de Prontidão")
            st.button("Registrar Treino")
            st.button("Avaliação Psicológica")
        
        with quick_access_col2:
            st.markdown("### Relatórios")
            st.button("Relatório Semanal")
            st.button("Análise de Tendências")
            st.button("Exportar Dados")

if __name__ == "__main__":
    main()
