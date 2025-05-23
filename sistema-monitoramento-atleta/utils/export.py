import io
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def export_to_excel(readiness_data, training_data, psychological_data):
    """
    Exporta os dados para um arquivo Excel com múltiplas abas
    
    Args:
        readiness_data: Lista de dicionários com dados de prontidão
        training_data: Lista de dicionários com dados de treino
        psychological_data: Lista de dicionários com dados psicológicos
    
    Returns:
        bytes: Arquivo Excel em formato de bytes
    """
    output = io.BytesIO()
    
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        # Aba de Prontidão
        if readiness_data:
            df_readiness = pd.DataFrame(readiness_data)
            df_readiness.to_excel(writer, sheet_name='Prontidão', index=False)
            
            # Formatação
            workbook = writer.book
            worksheet = writer.sheets['Prontidão']
            header_format = workbook.add_format({
                'bold': True,
                'bg_color': '#D3D3D3',
                'border': 1
            })
            
            for col_num, value in enumerate(df_readiness.columns.values):
                worksheet.write(0, col_num, value, header_format)
        
        # Aba de Treino
        if training_data:
            df_training = pd.DataFrame(training_data)
            df_training.to_excel(writer, sheet_name='Treino', index=False)
            
            worksheet = writer.sheets['Treino']
            for col_num, value in enumerate(df_training.columns.values):
                worksheet.write(0, col_num, value, header_format)
        
        # Aba de Avaliação Psicológica
        if psychological_data:
            df_psych = pd.DataFrame(psychological_data)
            df_psych.to_excel(writer, sheet_name='Psicológico', index=False)
            
            worksheet = writer.sheets['Psicológico']
            for col_num, value in enumerate(df_psych.columns.values):
                worksheet.write(0, col_num, value, header_format)
    
    output.seek(0)
    return output.getvalue()

def export_to_pdf(readiness_data, training_data, psychological_data, summary):
    """
    Exporta os dados para um arquivo PDF formatado
    
    Args:
        readiness_data: Lista de dicionários com dados de prontidão
        training_data: Lista de dicionários com dados de treino
        psychological_data: Lista de dicionários com dados psicológicos
        summary: Dicionário com métricas resumidas
    
    Returns:
        bytes: Arquivo PDF em formato de bytes
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []
    
    # Título
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30
    )
    elements.append(Paragraph("Relatório de Monitoramento do Atleta", title_style))
    elements.append(Spacer(1, 12))
    
    # Resumo
    if summary:
        elements.append(Paragraph("Resumo do Período", styles['Heading2']))
        elements.append(Spacer(1, 12))
        
        summary_data = [[k, f"{v:.2f}" if isinstance(v, float) else str(v)]
                       for k, v in summary.items()]
        
        summary_table = Table(summary_data)
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(summary_table)
        elements.append(Spacer(1, 20))
    
    # Dados de Prontidão
    if readiness_data:
        elements.append(Paragraph("Dados de Prontidão", styles['Heading2']))
        elements.append(Spacer(1, 12))
        
        df_readiness = pd.DataFrame(readiness_data)
        data = [df_readiness.columns.tolist()] + df_readiness.values.tolist()
        
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER')
        ]))
        elements.append(table)
        elements.append(Spacer(1, 20))
    
    # Dados de Treino
    if training_data:
        elements.append(Paragraph("Dados de Treino", styles['Heading2']))
        elements.append(Spacer(1, 12))
        
        df_training = pd.DataFrame(training_data)
        data = [df_training.columns.tolist()] + df_training.values.tolist()
        
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER')
        ]))
        elements.append(table)
        elements.append(Spacer(1, 20))
    
    # Dados Psicológicos
    if psychological_data:
        elements.append(Paragraph("Dados Psicológicos", styles['Heading2']))
        elements.append(Spacer(1, 12))
        
        df_psych = pd.DataFrame(psychological_data)
        data = [df_psych.columns.tolist()] + df_psych.values.tolist()
        
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER')
        ]))
        elements.append(table)
    
    # Gerar PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()
