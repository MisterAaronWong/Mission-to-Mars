# Import Splinter and BeautifulSoup and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

# 1. Initialize the browser.
# 2. Create a data dictionary.
# 3. End the WebDriver and return the scraped data.
# define this function as "scrape_all" and then initiate the browser
def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
# see the word "browser" here twice,
# one is the name of the variable passed into the function and the other is the name of a paramete
# Coding guidelines do not require that these match, even though they do in our current code.
# When we were testing our code in Jupyter, headless was set as False so we could see the scraping in action
# Now that we are deploying our code into a usable web app, we don't need to watch the script work
# (though it's totally okay if you still want to).
    
    # Next, we're going to set our news title and paragraph variables (remember, this function will return two values)
    news_title, news_paragraph = mars_news(browser)
        # tells Python that we'll be using our mars_news function to pull this data.
    
    # create the data dictionary
    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }
        # This dictionary does two things: It runs all of the functions we've created—featured_image(browser)
        # it also stores all of the results
        # When we create the HTML template, we'll create paths to the dictionary's values, which lets us present our data on our template
        # We're also adding the date the code was run last by adding "last_modified": dt.datetime.now()
        # For this line to work correctly, we'll also need to add import datetime as dt

    # Stop webdriver and return data
    browser.quit()
    return data 

# Set up Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser

    html = browser.html
    news_soup = soup(html, 'html.parser')

     # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


# ### Featured Images

def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        # find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    return img_url

### Mars Facts

def mars_facts():
    # Add try/except for error handling
    try:
      # use 'read_html" to scrape the facts table into a dataframe
      df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
      return None
    
    # Assign columns and set index of dataframe
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())