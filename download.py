import os, requests
from bs4 import BeautifulSoup

# Configuration parameters
filename = 'list-es.txt' #Change to file created with data list, using Excel workbook
SummaryText = "Resumen"   #Text to use for each chapter summary
OnlineText = "En línea"   #Text to use for web page link

# DO NOT CHANGE BELOW THIS LINE UNLESS YOU REALLY KNOW WHAT YOU'RE DOING
counter = 0
# Loads data list file.
datalist = open(filename, 'r',encoding='utf8').readlines()

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

    #get web data
    wp = requests.get(url)
    soup = BeautifulSoup(wp.content, 'html.parser')

    #Construct YAML heading for each md file
    mdFile = "---"  + "\n"
    mdFile += "title: " + ChapterName + "\n"
    mdFile += "tags: " + tags + "\n"
    mdFile += "cssclass: scriptures" + "\n"
    mdFile += "publish: false" + "\n"
    mdFile += "people:" + "\n"
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
        mdFile += "---" + "\n"
        mdFile += ChapterIntro.text + "\n" + "\n"
        mdFile += "---" + "\n" + "\n"
    
    # Adds Chapter summary, if there is one. Pulled from web.
    ChapterSummary = soup.find('p', class_='study-summary')
    if ChapterSummary != None:
        mdFile += "---" + "\n" + "__" + SummaryText + "__" + "\n"
        mdFile += ChapterSummary.text + "\n" + "\n"
        mdFile += "---" + "\n"

    ### Adds parragraphs/verses. Adding verse numbers if they exist Pulled from web. ###
    for verse in soup.find('div', class_='body-block').find_all('p'):
        verseNum = verse.find('span', class_='verse-number')
        if verseNum != None:
            mdFile += "###### " + verseNum.text + "\n"
        for TextToRemove in verse.find_all(['span', 'sup']):
            TextToRemove.clear()
        mdFile += verse.text  + "\n" + "\n"

    # Used in debugging
    #print(mdFile)

    # writes file
    if not os.path.exists(FolderPath):
        os.makedirs(FolderPath)
    outputfilename = (FolderPath + '/' + ChapterName).strip() + '.md'
    f = open(outputfilename, 'wb')
    n = f.write(mdFile.encode("utf-8"))
    f.close
    print("Saved " + outputfilename)

end_time = timeit.default_timer()
print("Processed " + counter + "files.")
input("Press any key to exit")
