import os, requests, win32clipboard
from bs4 import BeautifulSoup

# Set this to your root Obisidian library folder
# use forward slash and end in a forward slash (no backslashes)
#### CHANGE THIS LINE BEFORE USING ####
LibraryPath = "C:/Users/rfmar/Notes/Library/"

# Gets URL from clipboard
win32clipboard.OpenClipboard()
url = win32clipboard.GetClipboardData()
win32clipboard.CloseClipboard()

lang_code = url[-3:]

OnlineText = "Online"
if lang_code == "spa":
    OnlineText = "En línea"
elif lang_code == "por":
    OnlineText = "em linha"

# validates clipboard data, quits if not a Gospel Library address
gospel_library_snip = "www.churchofjesuschrist.org/study/"
if gospel_library_snip not in url:
    quit()

#Sets the folder name to start at the LibraryPath
FolderName = LibraryPath

#get web data
wp = requests.get(url)
soup = BeautifulSoup(wp.content, 'html.parser')



# Gets article name for title and file name
ArticleName = soup.find('title').text
#print(ArticleName)

# Verifies if article is a Gemeral Conference article
# Change if the church website ever changes the general conference link structure
gc_url_snip = "general-conference"
isGCarticle = gc_url_snip in url
if isGCarticle:
    position = url.find(gc_url_snip)
    GCyear = url[position + len(gc_url_snip) + 1:position + len(gc_url_snip) + 5]
    GCmonth = url[position + len(gc_url_snip) + 6:position + len(gc_url_snip) + 8]
    FolderName +=  "General Conference/" + GCyear + "-" + GCmonth + "/"
    #print(FolderName)

#Construct YAML heading for each md file
mdFile = "---"  + "\n"
mdFile += "title: " + ArticleName + "\n"
mdFile += "tags: " + "\n"
mdFile += "cssclass: scriptures" + "\n"
mdFile += "publish: false" + "\n"
mdFile += "people:" + "\n"
mdFile += "obsidianUIMode: preview" + "\n"
mdFile += "---" + "\n" + "\n"
#print(mdFile)

### Add chapter data for headings ###

# Adds chapter name
mdFile += "# " + ArticleName + "\n"

# Source link
mdFile += "[" + OnlineText + "](" + url + ")" + "\n" + "\n"

# Adds author if there is one
ArticleAuthor = soup.find('p', class_='author-name')
if ArticleAuthor != None:
    mdFile += ArticleAuthor.text + "\n"

# Adds role if there is one
ArticleAuthor = soup.find('p', class_='author-role')
if ArticleAuthor != None:
    mdFile += ArticleAuthor.text + "\n"

# Chapter subtitle if there is one
ChapterSubtitle = soup.find('p', class_='subtitle')
if ChapterSubtitle != None:
    mdFile += ChapterSubtitle.text + "\n" + "\n"

# Introduction if there is one (like the one on 1 Nephi 1)
ChapterIntro = soup.find('p', class_='intro')
if ChapterIntro != None:
    mdFile += "```" + "\n"
    mdFile += ChapterIntro.text + "\n"
    mdFile += "```" + "\n" + "\n"

# Adds Chapter summary, if there is one.
ChapterSummary = soup.find('p', class_='study-summary')
if ChapterSummary != None:
    mdFile += "> __" + SummaryText + "__" + "\n"
    mdFile += ChapterSummary.text + "\n" + "\n"

# Used in debugging
#print(mdFile)

### Adds parragraphs/verses. Adding verse numbers if they exist  ###
for verse in soup.find('div', class_='body-block').find_all(['p', 'h2', 'h3', 'h4']):
    verseNum = verse.find('span', class_='verse-number')
    if verseNum != None:
        mdFile += "###### " + verseNum.text + "\n"
    for TextToRemove in verse.find_all(['span', 'sup']):
        TextToRemove.clear()
    if verse.name == 'h2':
        mdFile += "## "
    elif verse.name == 'h3':
        mdFile += "### "
    elif verse.name == 'h4':
        mdFile += "#### "
    #replace square brakets with curly ones to avoid false links in Obsidian
    verseOutput = verse.text
    verseOutput = verseOutput.replace("[", "{")
    verseOutput = verseOutput.replace("]", "}")
    mdFile += verseOutput  + "\n" + "\n"

# Used in debugging
#print(mdFile)

# writes file
if not os.path.exists(FolderName):
    os.makedirs(FolderName)
outputfilename = (FolderName + ArticleName).strip() + '.md'
f = open(outputfilename, 'wb')
n = f.write(mdFile.encode("utf-8"))
f.close
print("Saved " + outputfilename)
