def calculate_training_load(duration, rpe):
    """
    Calcula a carga de treino usando o método RPE de Foster
    (Training Load = Duration x RPE)
    
    Args:
        duration: Duração do treino em minutos
        rpe: Rate of Perceived Exertion (1-10)
    
    Returns:
        float: Carga de treino em Unidades Arbitrárias (UA)
    """
    return duration * rpe

def calculate_acute_load(training_data):
    """
    Calcula a carga aguda (soma dos últimos 7 dias)
    
    Args:
        training_data: Lista de dicionários com dados de treino dos últimos 7 dias
    
    Returns:
        float: Carga aguda total
    """
    if not training_data:
        return 0
    
    return sum(session['training_load'] for session in training_data)

def calculate_chronic_load(training_data):
    """
    Calcula a carga crônica (média dos últimos 28 dias)
    
    Args:
        training_data: Lista de dicionários com dados de treino dos últimos 28 dias
    
    Returns:
        float: Carga crônica média
    """
    if not training_data:
        return 0
    
    total_load = sum(session['training_load'] for session in training_data)
    return total_load / len(training_data)

def calculate_acwr(acute_load, chronic_load):
    """
    Calcula o Acute:Chronic Workload Ratio (ACWR)
    
    Args:
        acute_load: Carga aguda (7 dias)
        chronic_load: Carga crônica (28 dias)
    
    Returns:
        float: ACWR (razão entre carga aguda e crônica)
    """
    if chronic_load == 0:
        return 0
    
    return acute_load / chronic_load

def interpret_acwr(acwr):
    """
    Interpreta o valor do ACWR e fornece recomendações
    
    Args:
        acwr: Acute:Chronic Workload Ratio
    
    Returns:
        tuple: (status, recomendação)
    """
    if acwr < 0.8:
        return ("Subcarga", 
                "O atleta está em subcarga. Considere aumentar gradualmente a intensidade dos treinos.")
    elif 0.8 <= acwr <= 1.3:
        return ("Zona Segura", 
                "O atleta está em uma zona segura de carga. Continue com o planejamento atual.")
    elif 1.3 < acwr <= 1.5:
        return ("Zona de Alerta", 
                "O atleta está entrando em uma zona de risco. Monitore de perto e considere reduzir a carga.")
    else:
        return ("Zona de Perigo", 
                "Risco elevado de lesão. Reduza a carga imediatamente e implemente recuperação ativa.")

def calculate_monotony(training_data):
    """
    Calcula a monotonia do treino (variabilidade diária)
    
    Args:
        training_data: Lista de dicionários com dados de treino da semana
    
    Returns:
        float: Índice de monotonia
    """
    if not training_data or len(training_data) < 2:
        return 0
    
    loads = [session['training_load'] for session in training_data]
    mean_load = sum(loads) / len(loads)
    
    # Cálculo do desvio padrão
    variance = sum((x - mean_load) ** 2 for x in loads) / len(loads)
    std_dev = variance ** 0.5
    
    # Monotonia = média diária / desvio padrão
    return mean_load / std_dev if std_dev > 0 else 0

def calculate_strain(training_load, monotony):
    """
    Calcula o strain (tensão) do treino
    
    Args:
        training_load: Carga total de treino
        monotony: Índice de monotonia
    
    Returns:
        float: Índice de strain
    """
    return training_load * monotony

def interpret_intensity_zone(zone):
    """
    Interpreta a zona de intensidade do treino
    
    Args:
        zone: String representando a zona de intensidade
    
    Returns:
        dict: Dicionário com descrição e recomendações
    """
    zones = {
        "Z1 - Recuperação": {
            "descrição": "Intensidade muito leve, foco em recuperação",
            "fc_alvo": "50-60% FCmax",
            "uso": "Recuperação ativa, aquecimento, volta à calma"
        },
        "Z2 - Base": {
            "descrição": "Intensidade leve, desenvolvimento aeróbio",
            "fc_alvo": "60-70% FCmax",
            "uso": "Treinos longos de base, desenvolvimento aeróbio"
        },
        "Z3 - Moderado": {
            "descrição": "Intensidade moderada",
            "fc_alvo": "70-80% FCmax",
            "uso": "Desenvolvimento de resistência aeróbia"
        },
        "Z4 - Limiar": {
            "descrição": "Intensidade alta, próxima ao limiar",
            "fc_alvo": "80-90% FCmax",
            "uso": "Desenvolvimento de limiar anaeróbio"
        },
        "Z5 - Máximo": {
            "descrição": "Intensidade máxima",
            "fc_alvo": "90-100% FCmax",
            "uso": "Desenvolvimento de potência anaeróbia"
        }
    }
    
    return zones.get(zone, {
        "descrição": "Zona não reconhecida",
        "fc_alvo": "Não definido",
        "uso": "Não definido"
    })

def suggest_next_training(recent_data):
    """
    Sugere o próximo treino com base nos dados recentes
    
    Args:
        recent_data: Dicionário com dados recentes do atleta
    
    Returns:
        dict: Sugestão de treino
    """
    if not recent_data:
        return {
            "tipo": "Moderado",
            "intensidade": "Z2 - Base",
            "duração": 60,
            "observações": "Começar com intensidade moderada para avaliação"
        }
    
    readiness = recent_data.get('readiness_score', 7)
    fatigue = recent_data.get('fatigue_level', 5)
    
    if readiness < 5 or fatigue > 7:
        return {
            "tipo": "Recuperação",
            "intensidade": "Z1 - Recuperação",
            "duração": 30,
            "observações": "Foco em recuperação devido à fadiga elevada"
        }
    elif readiness >= 8:
        return {
            "tipo": "Intenso",
            "intensidade": "Z4 - Limiar",
            "duração": 75,
            "observações": "Bom momento para treino de alta intensidade"
        }
    else:
        return {
            "tipo": "Normal",
            "intensidade": "Z3 - Moderado",
            "duração": 60,
            "observações": "Manter intensidade moderada para desenvolvimento"
        }
