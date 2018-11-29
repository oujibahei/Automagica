""" 
Open Excel and reads the searchterms it has to search for.
Opens Chrome and surfs to Google.com and enters searchterm.
Saves all the urls from the first page.
Writes the urls to excel.
"""

from automagica import *

excel_path = "C:\\Users\\hopyhuang\\Desktop\\Automagica\\examples\\multiprogram\\data.xlsx" #example: C:\\Users\Bob\\Desktop\\RPA Examples\\data.xlsx

# Read information from the excel in the second row, for columns 2 to 10
lookup_terms = []
for col in range(2,5):
    try:
        print(col)
        lookup_terms.append(ExcelReadCell(excel_path, "A"+str(col)))
    except Exception as e:
        print(e)

# Open Chrome
browser = ChromeBrowser()

for j,item in enumerate(lookup_terms):

    # Browse to Google
    browser.get('https://google.com')
    # Lookup the searchterm
    browser.find_element_by_xpath('//input[@name="q"]').send_keys(item)
    # Search
    browser.find_element_by_xpath('//input[@name="q"]').submit()
    # Get all found items
    articles = browser.find_elements_by_class_name("g")
    # Parse the headertexts to find the urls
    urls = []
    for article in articles:
        try:
            import re
            urls.append(re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', article.text)[0])
        except:
            pass

    # Write found urls to Excel
    for i,url in enumerate(urls):
        ExcelWriteRowCol(excel_path, r=j+2, c=i+2, write_value=url)

# Exit the browser
browser.quit()

# Open the Excel to show result
StartFile(excel_path)
