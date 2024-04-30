from datetime import datetime
import rssfeed

def get_formatted_date():
    # Get the current date
    current_date = datetime.now()

    # Define the translations for days of the week and months in Portuguese
    weekdays = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"]
    months = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]

    # Format the date
    formatted_date = "{}, {} de {} de {}".format(weekdays[current_date.weekday()], current_date.day, months[current_date.month - 1], current_date.year)

    return formatted_date

def generate_email_html():
    # Fetch new items from RSS feeds
    dr_items, gov_items, sns_items, infarmed_items = rssfeed.main()

    news_count = len(sns_items) + len(infarmed_items)
    dr_count = len(dr_items)
    gov_count = len(gov_items)
    infarmed_count = len(infarmed_items)

    # Estimate the reading time
    total_articles = news_count + dr_count + gov_count
    reading_time_minutes = total_articles * 2  # Assuming 2 minutes per article

    # Summary content
    summary_content = f"""
            Bom dia, as atualizações do dia incluem:
            <li><b>{dr_count}</b> publicações em Diário da República</li>
            <li><b>{gov_count}</b> comunicados do Governo</li>
            <li><b>{news_count}</b> artigos da DGS, SNS e Infarmed</li>
            <p>Tempo estimado de leitura: <b>{reading_time_minutes} minutos</b></p>
        """

    # Define your HTML template with placeholders for dynamic content
    with open("template.html", "r") as file:
        html_template = file.read()

    # Generate HTML content for SNS items
    sns_html = ""
    if len(sns_items) == 0 and len(infarmed_items) == 0:
        sns_html += "<p>Sem atualizações</p>"
    else:
        for item in sns_items:
            sns_html += "<p><a href='{}'>{}</a></p>".format(item["link"], item["title"])
        for item in infarmed_items:
            sns_html += "<p><a href='{}'>{}</a></p>".format(item["link"], item["title"])

    # Generate HTML content for DR items
    dr_html = ""
    if len(dr_items) == 0:
        dr_html += "<p>Sem atualizações</p>"
    else:
        for item in dr_items:
            dr_html += "<p>{}<br><a href='{}'>Ler mais</a></p>".format(item["title"], item["link"])

    # Generate HTML content for Gov items
    gov_html = ""
    if len(gov_items) == 0:
        gov_html += "<p>Sem atualizações</p>"
    else:
        for item in gov_items:
            gov_html += "<p><a href='{}'>{}</a></p>".format(item["link"], item["title"])


    # Replace placeholders with actual content
    html_content = html_template.replace("{summary_content}", summary_content)
    html_content = html_content.replace("{column1_content}", dr_html)
    html_content = html_content.replace("{column2_content}", gov_html)
    html_content = html_content.replace("{column3_content}", sns_html)
    html_content = html_content.replace("{datetime}", get_formatted_date())

    return html_content
