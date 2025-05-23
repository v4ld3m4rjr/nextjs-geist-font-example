def calculate_psychological_status(data):
    """
    Calcula o status psicológico geral com base em múltiplos indicadores
    
    Args:
        data: Dicionário com scores psicológicos
    
    Returns:
        str: Status psicológico geral
    """
    # Calcular média dos indicadores positivos
    positive_indicators = [
        data.get('intrinsic_motivation', 5),
        data.get('flow_score', 5),
        data.get('confidence_level', 5),
        data.get('focus_ability', 5),
        data.get('satisfaction_with_training', 5),
        data.get('team_cohesion', 5)
    ]
    positive_score = sum(positive_indicators) / len(positive_indicators)
    
    # Calcular média dos indicadores negativos
    negative_indicators = [
        data.get('depression_score', 5),
        data.get('anxiety_score', 5),
        data.get('stress_score', 5),
        data.get('amotivation', 5),
        data.get('pre_competition_anxiety', 5)
    ]
    negative_score = sum(negative_indicators) / len(negative_indicators)
    
    # Calcular score final (positivos - negativos + 5 para normalizar em escala de 0-10)
    final_score = positive_score - (negative_score / 2)
    
    if final_score >= 8:
        return "Excelente"
    elif final_score >= 6:
        return "Bom"
    elif final_score >= 4:
        return "Regular"
    else:
        return "Requer Atenção"

def interpret_stress_anxiety(stress_score, anxiety_score):
    """
    Interpreta os níveis de estresse e ansiedade
    
    Args:
        stress_score: Score de estresse (1-10)
        anxiety_score: Score de ansiedade (1-10)
    
    Returns:
        dict: Interpretação e recomendações
    """
    combined_score = (stress_score + anxiety_score) / 2
    
    if combined_score >= 8:
        return {
            "status": "Crítico",
            "recomendações": [
                "Consulta imediata com psicólogo esportivo",
                "Redução temporária da carga de treino",
                "Implementação de técnicas de relaxamento",
                "Foco em atividades de recuperação mental"
            ]
        }
    elif combined_score >= 6:
        return {
            "status": "Elevado",
            "recomendações": [
                "Monitoramento próximo dos níveis de estresse",
                "Prática regular de técnicas de respiração",
                "Considerar ajustes no planejamento de treino",
                "Aumentar atividades de lazer e recuperação"
            ]
        }
    elif combined_score >= 4:
        return {
            "status": "Moderado",
            "recomendações": [
                "Manter rotina de auto-monitoramento",
                "Prática de mindfulness",
                "Manter comunicação com equipe técnica"
            ]
        }
    else:
        return {
            "status": "Normal",
            "recomendações": [
                "Continuar com as práticas atuais",
                "Manter registro regular das emoções",
                "Praticar técnicas preventivas de gestão do estresse"
            ]
        }

def analyze_motivation(intrinsic_motivation, extrinsic_motivation, amotivation):
    """
    Analisa o perfil motivacional do atleta
    
    Args:
        intrinsic_motivation: Score de motivação intrínseca (1-10)
        extrinsic_motivation: Score de motivação extrínseca (1-10)
        amotivation: Score de desmotivação (1-10)
    
    Returns:
        dict: Análise do perfil motivacional e recomendações
    """
    motivation_profile = {
        "perfil": "",
        "recomendações": []
    }
    
    # Determinar perfil predominante
    if intrinsic_motivation > extrinsic_motivation:
        if intrinsic_motivation >= 7:
            motivation_profile["perfil"] = "Altamente Auto-Motivado"
            motivation_profile["recomendações"] = [
                "Manter autonomia nas decisões de treino",
                "Focar em objetivos de desenvolvimento pessoal",
                "Estimular criatividade nos treinos"
            ]
        else:
            motivation_profile["perfil"] = "Moderadamente Auto-Motivado"
            motivation_profile["recomendações"] = [
                "Reforçar conexão com objetivos pessoais",
                "Variar atividades para manter interesse",
                "Estabelecer metas de desenvolvimento"
            ]
    else:
        if extrinsic_motivation >= 7:
            motivation_profile["perfil"] = "Motivação Externa Forte"
            motivation_profile["recomendações"] = [
                "Desenvolver motivação intrínseca",
                "Identificar valores pessoais no esporte",
                "Reduzir foco em recompensas externas"
            ]
        else:
            motivation_profile["perfil"] = "Motivação Mista"
            motivation_profile["recomendações"] = [
                "Equilibrar objetivos internos e externos",
                "Desenvolver auto-consciência",
                "Estabelecer metas de curto e longo prazo"
            ]
    
    # Verificar desmotivação
    if amotivation >= 6:
        motivation_profile["perfil"] += " (Risco de Burnout)"
        motivation_profile["recomendações"].extend([
            "Intervenção psicológica recomendada",
            "Reavaliação de objetivos e expectativas",
            "Possível período de descanso necessário"
        ])
    
    return motivation_profile

def evaluate_competition_readiness(data):
    """
    Avalia a prontidão para competição com base em fatores psicológicos
    
    Args:
        data: Dicionário com dados psicológicos
    
    Returns:
        dict: Avaliação de prontidão e recomendações
    """
    # Pesos para diferentes fatores
    weights = {
        'confidence_level': 0.25,
        'focus_ability': 0.20,
        'emotional_state': 0.15,
        'pre_competition_anxiety': -0.20,
        'stress_score': -0.20
    }
    
    # Calcular score ponderado
    weighted_score = sum(data.get(key, 5) * weight for key, weight in weights.items())
    normalized_score = (weighted_score + 10) / 2  # Normalizar para escala 0-10
    
    if normalized_score >= 8:
        return {
            "status": "Pronto para Competição",
            "score": normalized_score,
            "recomendações": [
                "Manter rotina de preparação mental",
                "Focar em visualização positiva",
                "Revisar estratégias de competição"
            ]
        }
    elif normalized_score >= 6:
        return {
            "status": "Moderadamente Pronto",
            "score": normalized_score,
            "recomendações": [
                "Intensificar práticas de gestão da ansiedade",
                "Reforçar confiança através de treinos específicos",
                "Manter comunicação com equipe técnica"
            ]
        }
    else:
        return {
            "status": "Requer Preparação Adicional",
            "score": normalized_score,
            "recomendações": [
                "Intervenção psicológica recomendada",
                "Ajustar expectativas e objetivos",
                "Focar em aspectos básicos de preparação mental"
            ]
        }

def suggest_psychological_interventions(data):
    """
    Sugere intervenções psicológicas baseadas no perfil do atleta
    
    Args:
        data: Dicionário com dados psicológicos
    
    Returns:
        list: Lista de intervenções sugeridas
    """
    interventions = []
    
    # Verificar diferentes aspectos e adicionar intervenções relevantes
    if data.get('stress_score', 0) > 6 or data.get('anxiety_score', 0) > 6:
        interventions.extend([
            "Técnicas de Respiração Profunda",
            "Meditação Mindfulness",
            "Relaxamento Muscular Progressivo"
        ])
    
    if data.get('confidence_level', 10) < 6:
        interventions.extend([
            "Visualização Positiva",
            "Diário de Sucessos",
            "Estabelecimento de Metas Progressivas"
        ])
    
    if data.get('focus_ability', 10) < 6:
        interventions.extend([
            "Exercícios de Concentração",
            "Técnicas de Ancoragem",
            "Rotinas Pré-Performance"
        ])
    
    if data.get('team_cohesion', 10) < 6:
        interventions.extend([
            "Atividades de Team Building",
            "Comunicação Assertiva",
            "Definição de Papéis e Responsabilidades"
        ])
    
    # Adicionar intervenções gerais se lista estiver vazia
    if not interventions:
        interventions = [
            "Manutenção de Rotina Mental",
            "Prática Regular de Mindfulness",
            "Auto-Monitoramento Emocional"
        ]
    
    return interventions
