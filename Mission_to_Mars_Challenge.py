#!/usr/bin/env python
# coding: utf-8

# ### Article Scraping

# In[1]:


# import dependencies

# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd


# In[2]:


# set your executable path
# then set up the URL (NASA Mars News (Links to an external site.)) for scraping
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[3]:


# assign the url and instruct the browser to visit it

# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

# 2nd line accomplishing two things:
    # 1. we're searching for elements with a specific combination of tag (div) and attribute (list_text
        # eg. ul.item_list would be found in HTML as <ul class="item_list">
    # 2. we're also telling our browser to wait one second before searching for components
        # optional delay is useful because sometimes dynamic pages take a little while to load, especially if they are image-heavy


# In[4]:


# set up the HTML parser:

html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')

# 3rd line: we've assigned slide_elem as the variable to look for the <div /> tag
    # and its descendent (the other tags within the <div /> element)
    # This is our parent element
    # this element holds all of the other elements within it, and we'll reference it when we want to filter search results even further
    # The . is used for selecting classes, such as list_text, so the code 'div.list_text' pinpoints the <div /> tag with the class of list_text
# CSS works from right to left, such as returning the last item on the list instead of the first
# therefore: when using select_one, the first matching element returned will be a <li /> element with a class of slide and all nested elements within it


# In[5]:


# assign the title and summary text to variables we'll reference later. let's begin our scraping

slide_elem.find('div', class_='content_title')

# we chained .find onto our previously assigned variable, slide_elem.
# we're saying, "This variable holds a ton of information, so look inside of that information to find this specific data."
# we're looking for the content title, specified by saying, "The specific data is in a <div /> with a class of 'content_title'."
# The output should be the HTML containing the content title and anything else nested inside of that <div />


# In[6]:


# The title is in that mix of HTML in our output. But we need to get just the text, and the extra HTML stuff isn't necessary

# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# We've added .get_text(). When this new method is chained onto .find(), only the text of the element is returned.
# The code above, for example, would return only the title of the news article and not any of the HTML tags or elements
# the result is the most recent title published on the website.
# When the website is updated and a new article is posted, when our code is run again, it will return that article instead


# In[7]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# In[8]:


# set up the URL

# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# ### Featured Images

# In[9]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1] # new variable holds scraping results = browser fins an elemnt by its tag
full_image_elem.click() # Splinter will "click" the image to view its full size 


# In[10]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[11]:


# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# An img tag is nested within this HTML, so we've included it.
# .get('src') pulls the link to the image
# What we've done here is tell BeautifulSoup to look inside the <img /> tag for an image with a class of fancybox-image
# Basically we're saying, "This is where the image we want lives—use the link that's inside these tags."
# We pulled the link to the image by pointing BeautifulSoup to where the image will be, instead of grabbing the URL directly
# when JPL updates its image page, our code will still pull the most recent image
# if we copy and paste this link into a browser, it won't work
# because it's only a partial link, as the base URL isn't included
# Look at our address bar in the webpage, we can see the entire URL up there already;
# we just need to add the first portion to our app.


# In[12]:


# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url

# img_irl = this variable holds our f string
# f'https://spaceimages-mars.com/ = an f-string, a type of string formatting used for print statements in Python.
# {img_url_rel} = The curly brackets hold a variable that will be inserted into the f-string when it's executed

# We're using an f-string for this print statement because it's a cleaner way to create print statements;
# they're also evaluated at run-time
# This means that it, and the variable it holds, doesn't exist until the code is executed and the values are not constant.
# This works well for our scraping app because the data we're scraping is live and will be updated frequently.


# In[13]:


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df

# 1 - creating a new DataFrame from the HTML table
    # The Pandas function read_html() specifically searches for and returns a list of tables found in the HTML
    # By specifying an index of 0, we're telling Pandas to pull only the first table it encounters, or the first item in the list.
    # Then, it turns the table into a DataFrame.
# 2 - we assign columns to the new DataFrame for additional clarity.
# 3 - By using the .set_index() function, we're turning the Description column into the DataFrame's index
 # inplace=True means that the updated index will remain in place, without having to reassign the DataFrame to a new variable
# 4 - call the DataFrame, we're presented with a tidy, Pandas-friendly representation of the HTML table we were just viewing on the website


# In[14]:


# easily convert DF back to html-ready code
df.to_html()

# The result is a slightly confusing-looking set of HTML code—it's a <table /> element with a lot of nested elements
# adding this exact block of code to Robin's web app, the data it's storing will be presented in an easy-to-read tabular format.


# In[15]:


# end the automated browsing session.
# Without it, the automated browser won't know to shut down
# it will continue to listen for instructions and use the computer's resources
# (it may put a strain on memory or a laptop's battery if left on)
# We really only want the automated browser to remain active while we're scraping data.
browser.quit()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[16]:


# import dependencies

# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd


# In[17]:


# set your executable path
# then set up the URL (NASA Mars News (Links to an external site.)) for scraping
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[18]:


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com'
browser.visit(url)


# In[19]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
for x in range(0, 4):
    # Browse through each page w/ Enhanced in the partial text
    browser.links.find_by_partial_text('Enhanced')[x].click()
    
    # Parse the HTML
    html = browser.html
    imgurl_soup = soup(html,'html.parser')
    
    # Scraping
    title = imgurl_soup.find('h2', class_='title').text
    img_url = imgurl_soup.find('li').a.get('href')
    
    # Store results into the empty hemispheres dictionary
    hemispheres = {}
    hemispheres['img_url'] = f'https://marshemispheres.com/{img_url}'
    hemispheres['title'] = title
    hemisphere_image_urls.append(hemispheres)
    
    # Browse back to repeat for all 4 pages
    browser.back()


# In[20]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[21]:


# 5. Quit the browser
browser.quit()


# In[ ]:




