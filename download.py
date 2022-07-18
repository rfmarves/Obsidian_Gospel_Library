import os, requests
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options

# Configuration parameters
filename = 'listTEST.txt' #Change to file created with data list, using Excel workbook

LangList = ["eng", "spa", "por"]                        #Language Code list
SummaryTextList = ["Summary", "Resumen", "Resumo"]      #Text to use for each chapter summary
OnlineTextList = [ "Online", "en línea", "em linha"]    #Text to use for web page link

# DO NOT CHANGE BELOW THIS LINE UNLESS YOU KNOW WHAT YOU'RE DOING
counter = 0
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',
    'X-Requested-With': 'XMLHttpRequest',
}
# Loads data list file.
datalist = open(filename, 'r', encoding='utf8').readlines()

# Loops through all the files
for line in datalist:
    #load variables from file
    counter += 1
    linedata = line.split("|")
    #print(linedata)
    url = linedata[0]
    FolderPath = linedata[1]
    ChapterName = linedata[2]
    BookName = linedata[3]
    PreviousChapter = linedata[4]
    NextChapter = linedata[5]
    tags = linedata[6]
    
    LangCode = LangList.index(url[-3:])
    SummaryText = SummaryTextList[LangCode]
    OnlineText = OnlineTextList[LangCode]

    chrome_options = Options()
    chrome_options.add_argument("--headless") # Opens the browser up in background

    #get web data
    outputfilename = (FolderPath + '/' + ChapterName).strip() + '.md'
    print(str(counter) + ":Getting " + outputfilename)

    with Chrome(options=chrome_options) as browser:
        browser.get(url)
        wp = browser.page_source

##    AttemptCount = 0
##    while True:
##        AttemptCount += 1
##
##        with Chrome(options=chrome_options) as browser:
##            browser.get(url)
##            wp = browser.page_source
##        print(wp)    
##        #wp = requests.get(url, headers=headers)
##        if wp.ok:
##            break
##        if AttemptCount > 11:
##            print("Failed dowloading after 10 attempts")
##            break
##        if AttemptCount > 1:
##            print("Download attempt " + str(AttemptCount))

    soup = BeautifulSoup(wp, 'html.parser')

    #Construct YAML heading for each md file
    mdFile = "---"  + "\n"
    mdFile += "title: " + ChapterName + "\n"
    mdFile += "tags: " + tags + "\n"
    mdFile += "cssclass: scriptures" + "\n"
    mdFile += "publish: false" + "\n"
    mdFile += "people:" + "\n"
    mdFile += "obsidianUIMode: preview" + "\n"
    mdFile += "---" + "\n" + "\n"
    
    ### Add chapter data for headings ###

    # Adds chapter name
    mdFile += "# " + ChapterName + "\n"
    
    # Chapter navigation, based on excel file
    if len(PreviousChapter) > 1:
        mdFile += "[[" + PreviousChapter + "| <-- " + PreviousChapter + "]] "
    mdFile += "| [[" + BookName + "]] |"
    if len(NextChapter) > 1:
        mdFile += " [[" + NextChapter + "|" + NextChapter + " --> ]]"
    mdFile += "\n" + "\n"
    mdFile += "[" + OnlineText + "](" + url + ")" + "\n" + "\n"
    
    # Chapter subtitle if there is one, pulled from web
    ChapterSubtitle = soup.find('p', class_='subtitle')
    if ChapterSubtitle != None:
        mdFile += BookName + "\n"
        mdFile += ChapterSubtitle.text + "\n" + "\n"
    
    # Introduction if there is one (like the one on 1 Nephi 1), pulled from web
    ChapterIntro = soup.find('p', class_='intro')
    if ChapterIntro != None:
        mdFile += "```" + "\n"
        mdFile += ChapterIntro.text + "\n"
        mdFile += "```" + "\n" + "\n"
    
    # Adds Chapter summary, if there is one. Pulled from web.
    ChapterSummary = soup.find('p', class_='study-summary')
    if ChapterSummary != None:
        mdFile += "> __" + SummaryText + "__" + "\n"
        mdFile += ChapterSummary.text + "\n" + "\n"

    ### Adds parragraphs/verses. Adding verse numbers if they exist Pulled from web. ###
    for verse in soup.find('div', class_='body-block').find_all('p'):
        verseNum = verse.find('span', class_='verse-number')
        if verseNum != None:
            mdFile += "###### " + verseNum.text + "\n"
            for TextToRemove in verse.find_all('span', class_='verse-number'):
                TextToRemove.clear()
        for TextToRemove in verse.find_all(['sup']):
            TextToRemove.clear()
        mdFile += verse.get_text("\n")  + "\n" + "\n"

    # Used in debuggingr
    #print(mdFile)

    # writes file
    if not os.path.exists(FolderPath):
        os.makedirs(FolderPath)
    f = open(outputfilename, 'wb')
    n = f.write(mdFile.encode("utf-8"))
    f.close
    print("File saved" + "\n")

print("Processed " + counter + "files.")
input("Press any key to exit")
