import gspread
from oauth2client.service_account import ServiceAccountCredentials
from bs4 import BeautifulSoup

# --- Google Sheets Configuration ---
# You will need to create a service account and share your Google Sheet with it.
# See the instructions in the README for more details.
SCOPE = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
CREDS_FILE = 'client_secret.json'
SHEET_NAME = 'Lab News'

# --- HTML Template Configuration ---
TEMPLATE_FILE = 'news.html'
NEWS_CONTAINER_ID = 'news-container'

def get_news_data():
    """
    Fetches news data from the specified Google Sheet.
    """
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, SCOPE)
    client = gspread.authorize(creds)
    sheet = client.open(SHEET_NAME).sheet1
    return sheet.get_all_records()

def create_news_item_html(news_item):
    """
    Creates the HTML for a single news item.
    """
    return f"""
    <div class="card">
        <h2 class="typography_h2">{news_item['Headline']}</h2>
        <p class="typography_body text-sm text-gray-500 mb-4">{news_item['Date']}</p>
        <p class="typography_body">{news_item['Content']}</p>
    </div>
    """

def main():
    """
    Main function to update the news page.
    """
    # Read the HTML template
    with open(TEMPLATE_FILE, 'r') as f:
        soup = BeautifulSoup(f, 'html.parser')

    # Get the news data
    news_data = get_news_data()

    # Find the news container
    news_container = soup.find(id=NEWS_CONTAINER_ID)

    # Clear the news container
    news_container.clear()

    # Generate and inject the HTML for each news item
    for news_item in news_data:
        news_item_html = create_news_item_html(news_item)
        news_container.append(BeautifulSoup(news_item_html, 'html.parser'))

    # Write the updated HTML back to the file
    with open(TEMPLATE_FILE, 'w') as f:
        f.write(str(soup))

if __name__ == '__main__':
    main() 