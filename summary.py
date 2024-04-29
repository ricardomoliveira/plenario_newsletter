from transformers import pipeline


def summarize_news(news_list):
    # Extract titles and descriptions
    titles = [news['title'] for news in news_list]
    descriptions = [news['description'] for news in news_list]

    # Combine titles and descriptions into a single string
    content = ' '.join(titles + descriptions)

    # Initialize the summarization pipeline for Portuguese
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn", tokenizer="facebook/bart-large-cnn")

    # Generate the summary
    summary = summarizer(content, max_length=150, min_length=30, do_sample=False)

    return summary[0]['summary_text']


# Example usage
news_list = [{'title': 'Abertas 322 vagas com incentivos para fixar médicos em zonas carenciadas', 'description': 'Reforço insere-se na estratégia do Governo de valorização do SNS e dos seus recursos humanos.', 'link': 'https://www.sns.gov.pt/noticias/2024/03/28/abertas-322-vagas-com-incentivos-para-fixar-medicos-em-zonas-carenciadas/'}, {'title': 'Urgência de Águeda com novas instalações', 'description': 'Ministro da Saúde visitou Hospital Conde de Sucena. ', 'link': 'https://www.sns.gov.pt/noticias/2024/03/28/898399/'}, {'title': 'Centro de Saúde de Albergaria-a-Velha renovado', 'description': 'Ministro da Saúde, Manuel Pizarro, inaugurou requalificação do PRR', 'link': 'https://www.sns.gov.pt/noticias/2024/03/28/centro-de-saude-de-albergaria-a-velha-renovado/'}, {'title': 'A saúde na proteção das crianças e jovens', 'description': 'Grupo de trabalho constituído pela Secretária de Estado da Promoção da Saúde apresentou propostas.', 'link': 'https://www.sns.gov.pt/noticias/2024/03/25/a-saude-na-protecao-das-criancas-e-jovens/'}, {'title': 'Top Health Awards 2024', 'description': 'Projeto Farol no IPO do Porto vence na categoria de Sustentabilidade Social', 'link': 'https://www.sns.gov.pt/noticias/2024/03/25/top-health-awards-2024/'}, {'title': 'Ecossistema Seguro de Dados de Saúde', 'description': 'ULS Coimbra começa a pilotar o Espaço Europeu de Dados de Saúde em Portugal', 'link': 'https://www.sns.gov.pt/noticias/2024/03/25/ecossistema-seguro-de-dados-de-saude/'}, {'title': 'Governo reforça Programa Nacional de Vacinação', 'description': 'No último ano foram administradas mais de 7 milhões de vacinas em Portugal no âmbito do PNV.', 'link': 'https://www.sns.gov.pt/noticias/2024/03/22/governo-reforca-programa-nacional-de-vacinacao/'}, {'title': 'Urgência de Psiquiatria da ULS do Oeste entra em funcionamento', 'description': 'Novo serviço do Hospital das Caldas da Rainha inicia dia 25 de março.', 'link': 'https://www.sns.gov.pt/noticias/2024/03/22/urgencia-de-psiquiatria-da-uls-do-oeste-entra-em-funcionamento/'}, {'title': 'Radiologia de intervenção na ULS Alto Ave', 'description': 'Hospital da Senhora da Oliveira - Guimarães alarga o leque de procedimentos e disponibiliza novos tratamentos', 'link': 'https://www.sns.gov.pt/noticias/2024/03/22/radiologia-de-intervencao-na-uls-alto-ave/'}, {'title': 'Médica Conceição Margalha distinguida com medalha de ouro', 'description': 'Homenagem foi feita pelo Secretário de Estado da Saúde em visita a Beja', 'link': 'https://www.sns.gov.pt/noticias/2024/03/21/medica-conceicao-margalha-distinguida-com-medalha-de-ouro/'}]


summary = summarize_news(news_list)
print(summary)
