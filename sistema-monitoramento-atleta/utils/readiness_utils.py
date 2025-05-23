def calculate_readiness_score(data):
    # Placeholder for readiness score calculation logic
    score = 0
    # Example: weighted sum of factors
    score += data.get('sleep_quality', 0) * 0.2
    score += data.get('sleep_duration', 0) * 0.1
    score += (10 - data.get('stress_level', 0)) * 0.2
    score += (10 - data.get('muscle_soreness', 0)) * 0.2
    score += data.get('energy_level', 0) * 0.2
    score += data.get('motivation', 0) * 0.1
    return score

def interpret_readiness_score(score):
    if score >= 8:
        return "Excelente prontidão"
    elif score >= 5:
        return "Prontidão moderada"
    else:
        return "Prontidão baixa"
