from seleniumbase import SB  # Import SeleniumBase library
from bs4 import BeautifulSoup  # Import BeautifulSoup for HTML parsing
import time  # Import time library for sleep delays (not ideal, see notes below)
import boto3  # Import boto3 library for interacting with DynamoDB

def open_the_turnstile_page(sb, url):
    """
    Opens the specified URL in the browser using SeleniumBase with reconnect handling.

    Args:
        sb (SB): The SeleniumBase instance.
        url (str): The URL to open.
    """
    sb.driver.uc_open_with_reconnect(url, reconnect_time=2)  # Open with reconnect
    if not sb.is_text_visible("Find your dream remote job without the hassle"):
        # If text not found, retry opening with longer timeout
        sb.driver.uc_open_with_reconnect(url, 4)

def click_turnstile_and_verify(sb):
    """
    Clicks on the turnstile element and verifies successful completion.

    Args:
        sb (SB): The SeleniumBase instance.
    """
    sb.driver.switch_to_frame("iframe")  # Switch to the iframe containing the turnstile
    time.sleep(2)  # Wait for 2 seconds (replace with WebDriverWait if possible)
    sb.driver.uc_click("span")  # Click on the turnstile element
    time.sleep(3)  # Wait for 3 seconds (replace with WebDriverWait if possible)
    sb.assert_text_not_visible("Verify you are human by completing the action below.", timeout=10)  # Verify human verification is complete

def scrapeData(soup):
    """
    Scrapes job data from the provided BeautifulSoup object.

    Args:
        soup (BeautifulSoup): The BeautifulSoup object representing the HTML content.

    Returns:
        list: A list of dictionaries containing scraped job data.
    """
    data = []
    for job in soup.find_all('div', {"class": "job-tile"}):
        obj = {}
        anchor = job.find('a', {'class': 'remotive-url-visit'})
        jobData = anchor.find_all('span')
        obj['job_title'] = jobData[0].text
        obj['company'] = jobData[2].text
        obj['description_url'] = 'remotive.com' + anchor.get('href')
        locations = job.find_all('span', {"class": "job-tile-location"})
        obj['locations'] = list(map(lambda l: l.text.replace('\n', '').strip(), locations))

        data.append(obj)
    return data

def storeData(data):
    """
    Stores scraped job data into a DynamoDB table.

    Args:
        data (list): A list of dictionaries containing job data.
    """
    # Replace with your table name and data
    table_name = "my_table"

    # Configure boto3
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)

    # Convert data to DynamoDB format
    formatted_data = []
    for item in data:
        dynamo_item = {}
        for key, value in item.items():
            if key == "locations":
                dynamo_item[key] = {"L": [{"S": loc} for loc in value]}  # List of strings
            else:
                dynamo_item[key] = {"S": value}  # String data type
        formatted_data.append(dynamo_item)

    # Write data to DynamoDB
    for item in formatted_data:
        table.put_item(Item=item)

    print("Data inserted successfully!")

# Main function
if __name__ == '__main__':
    with SB(uc=True, test=True) as sb:
        open_the_turnstile_page(sb, "remotive.com")
        try:
            click_turnstile_and_verify(sb)
        except Exception:
            open_the_turnstile_page(sb, "remotive.com")
            click_turnstile_and_verify(sb)

        soup = BeautifulSoup(sb.get_page_source(), 'html.parser')

        scrapedData = scrapeData(soup) # Scrapting the data from remotive.com
        print(scrapedData)
        storeData(scrapedData)
