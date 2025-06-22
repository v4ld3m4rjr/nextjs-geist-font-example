import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from streamlit import session_state as state

# Configuração da página
st.set_page_config(
    page_title="Estatísticas de Futebol em Tempo Real",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo personalizado
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        margin-bottom: 0.5rem;
    }
    .stat-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f0f2f6;
        margin-bottom: 1rem;
    }
    div[data-testid="stSidebarNav"] {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    .scoreboard {
        background-color: #1a1a1a;
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
        margin-bottom: 2rem;
    }
    .score {
        font-size: 2.5rem;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Inicialização do estado da sessão
if 'times' not in st.session_state:
    st.session_state.times = {
        'Time A': [],
        'Time B': []
    }
    
if 'estatisticas' not in st.session_state:
    st.session_state.estatisticas = pd.DataFrame(columns=[
        'Jogador', 'Time', 'Gols', 'Passes Certos', 'Passes Errados', 
        'Distância (km)', 'Chutes a Gol', 'Última Atualização'
    ])

if 'placar' not in st.session_state:
    st.session_state.placar = {'Time A': 0, 'Time B': 0}

# Função para adicionar jogador
def adicionar_jogador(time, nome, numero):
    if nome and numero:
        # Verificar se o número já existe no time
        numeros_existentes = [j.get('numero') for j in st.session_state.times[time]]
        if numero in numeros_existentes:
            st.error(f"Número {numero} já existe no {time}")
            return False
        
        # Verificar se o nome já existe
        nomes_existentes = [j.get('nome') for j in st.session_state.times[time]]
        if nome in nomes_existentes:
            st.error(f"Jogador {nome} já existe no {time}")
            return False
        
        st.session_state.times[time].append({
            'nome': nome,
            'numero': numero,
            'gols': 0,
            'passes_certos': 0,
            'passes_errados': 0,
            'distancia': 0.0,
            'chutes_gol': 0
        })
        atualizar_estatisticas()
        return True
    return False

# Função para atualizar estatísticas
def atualizar_estatisticas():
    dados = []
    for time, jogadores in st.session_state.times.items():
        for jogador in jogadores:
            total_passes = jogador['passes_certos'] + jogador['passes_errados']
            precisao = (jogador['passes_certos'] / total_passes * 100) if total_passes > 0 else 0
            
            dados.append({
                'Jogador': f"{jogador['numero']} - {jogador['nome']}",
                'Time': time,
                'Gols': jogador['gols'],
                'Passes Certos': jogador['passes_certos'],
                'Passes Errados': jogador['passes_errados'],
                'Precisão de Passes (%)': round(precisao, 1),
                'Distância (km)': round(jogador['distancia'], 2),
                'Chutes a Gol': jogador['chutes_gol'],
                'Última Atualização': datetime.now().strftime('%H:%M:%S')
            })
    st.session_state.estatisticas = pd.DataFrame(dados)

# Interface principal
st.title("⚽ Estatísticas de Futebol em Tempo Real")

# Placar
st.markdown("""
    <div class="scoreboard">
        <h2>PLACAR</h2>
        <div class="score">
            Time A {0} x {1} Time B
        </div>
    </div>
""".format(st.session_state.placar['Time A'], st.session_state.placar['Time B']), unsafe_allow_html=True)

# Sidebar para gerenciamento de times
with st.sidebar:
    st.header("Gerenciamento de Times")
    
    # Time A
    st.subheader("Time A")
    with st.form("form_time_a"):
        nome_a = st.text_input("Nome do Jogador (Time A)", key="nome_a")
        numero_a = st.number_input("Número da Camisa (Time A)", min_value=1, max_value=99, step=1, key="numero_a")
        submit_a = st.form_submit_button("Adicionar ao Time A")
        if submit_a:
            if adicionar_jogador("Time A", nome_a, int(numero_a)):
                st.session_state.nome_a = ""
                st.session_state.numero_a = 1
    
    # Time B
    st.subheader("Time B")
    with st.form("form_time_b"):
        nome_b = st.text_input("Nome do Jogador (Time B)", key="nome_b")
        numero_b = st.number_input("Número da Camisa (Time B)", min_value=1, max_value=99, step=1, key="numero_b")
        submit_b = st.form_submit_button("Adicionar ao Time B")
        if submit_b:
            if adicionar_jogador("Time B", nome_b, int(numero_b)):
                st.session_state.nome_b = ""
                st.session_state.numero_b = 1

# Área principal
if st.session_state.times['Time A'] or st.session_state.times['Time B']:
    # Seleção de jogador para atualização
    col_select, col_stats = st.columns([1, 3])
    
    with col_select:
        st.subheader("Selecionar Jogador")
        todos_jogadores = [(f"{j['numero']} - {j['nome']}", time, j) 
                          for time, jogadores in st.session_state.times.items() 
                          for j in jogadores]
        
        if todos_jogadores:
            jogador_display = st.selectbox(
                "Jogador",
                options=[f"{j[0]} ({j[1]})" for j in todos_jogadores],
                key="jogador_select"
            )
            idx = [f"{j[0]} ({j[1]})" for j in todos_jogadores].index(jogador_display)
            jogador_atual = todos_jogadores[idx][2]
            time_atual = todos_jogadores[idx][1]
            
            # Mostrar estatísticas do jogador selecionado
            st.markdown("### Estatísticas Atuais")
            total_passes = jogador_atual['passes_certos'] + jogador_atual['passes_errados']
            precisao = (jogador_atual['passes_certos'] / total_passes * 100) if total_passes > 0 else 0
            
            st.markdown(f"""
                * Gols: {jogador_atual['gols']}
                * Passes Certos: {jogador_atual['passes_certos']}
                * Passes Errados: {jogador_atual['passes_errados']}
                * Precisão de Passes: {precisao:.1f}%
                * Chutes a Gol: {jogador_atual['chutes_gol']}
                * Distância: {jogador_atual['distancia']:.2f} km
            """)
    
    with col_stats:
        st.subheader("Atualizar Estatísticas")
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            if st.button("⚽ GOL!", use_container_width=True):
                jogador_atual['gols'] += 1
                st.session_state.placar[time_atual] += 1
                atualizar_estatisticas()
            if st.button("↩️ Remover Gol", use_container_width=True):
                if jogador_atual['gols'] > 0:
                    jogador_atual['gols'] -= 1
                    st.session_state.placar[time_atual] -= 1
                    atualizar_estatisticas()
        
        with col2:
            if st.button("➕ Passe Certo", use_container_width=True):
                jogador_atual['passes_certos'] += 1
                atualizar_estatisticas()
            if st.button("➖ Passe Certo", use_container_width=True):
                jogador_atual['passes_certos'] = max(0, jogador_atual['passes_certos'] - 1)
                atualizar_estatisticas()
        
        with col3:
            if st.button("➕ Passe Errado", use_container_width=True):
                jogador_atual['passes_errados'] += 1
                atualizar_estatisticas()
            if st.button("➖ Passe Errado", use_container_width=True):
                jogador_atual['passes_errados'] = max(0, jogador_atual['passes_errados'] - 1)
                atualizar_estatisticas()
        
        with col4:
            if st.button("➕ Chute a Gol", use_container_width=True):
                jogador_atual['chutes_gol'] += 1
                atualizar_estatisticas()
            if st.button("➖ Chute a Gol", use_container_width=True):
                jogador_atual['chutes_gol'] = max(0, jogador_atual['chutes_gol'] - 1)
                atualizar_estatisticas()
        
        with col5:
            dist = st.number_input("Distância (km)", min_value=0.0, step=0.1)
            if st.button("Adicionar Distância", use_container_width=True):
                jogador_atual['distancia'] += dist
                atualizar_estatisticas()

    # Exibição das Estatísticas
    st.header("Estatísticas da Partida")

    if not st.session_state.estatisticas.empty:
        tab1, tab2, tab3 = st.tabs(["Estatísticas por Time", "Estatísticas Individuais", "Gráficos"])
        
        with tab1:
            # Estatísticas por Time
            stats_time = st.session_state.estatisticas.groupby('Time').agg({
                'Gols': 'sum',
                'Passes Certos': 'sum',
                'Passes Errados': 'sum',
                'Distância (km)': 'sum',
                'Chutes a Gol': 'sum'
            }).reset_index()
            
            # Calcular percentual de passes certos
            stats_time['Precisão de Passes (%)'] = (stats_time['Passes Certos'] / 
                (stats_time['Passes Certos'] + stats_time['Passes Errados']) * 100).round(1)
            
            st.dataframe(stats_time, use_container_width=True)
        
        with tab2:
            # Estatísticas Individuais
            st.dataframe(st.session_state.estatisticas, use_container_width=True)
        
        with tab3:
            col1, col2 = st.columns(2)
            
            with col1:
                # Gráfico de Passes por Time
                fig_passes = px.bar(
                    stats_time,
                    x='Time',
                    y=['Passes Certos', 'Passes Errados'],
                    title='Passes por Time',
                    barmode='group'
                )
                st.plotly_chart(fig_passes, use_container_width=True)
            
            with col2:
                # Gráfico de Gols por Jogador
                fig_gols = px.bar(
                    st.session_state.estatisticas,
                    x='Jogador',
                    y='Gols',
                    color='Time',
                    title='Gols por Jogador'
                )
                fig_gols.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig_gols, use_container_width=True)

    # Botão para Reiniciar Estatísticas
    if st.button("🔄 Reiniciar Todas as Estatísticas", type="primary"):
        st.session_state.times = {'Time A': [], 'Time B': []}
        st.session_state.estatisticas = pd.DataFrame(columns=[
            'Jogador', 'Time', 'Gols', 'Passes Certos', 'Passes Errados', 
            'Distância (km)', 'Chutes a Gol', 'Última Atualização'
        ])
        st.session_state.placar = {'Time A': 0, 'Time B': 0}
        st.experimental_rerun()
else:
    st.info("Adicione jogadores aos times usando o menu lateral para começar a registrar estatísticas.")
