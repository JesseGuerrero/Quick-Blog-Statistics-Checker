import requests
from bs4 import BeautifulSoup

headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36' }
def get_text(url, contentClass):
    global headers
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, "html.parser")
    text = ' '.join(map(lambda p: p.text, soup.find_all(class_=contentClass)))
    return soup.title.text, text


def getBlogStatistics(siteMapURLs: list, siteIdentifier: str, contentClass: str) -> None:
    global headers
    urls = []

    for siteMapURL in siteMapURLs:
        sitemap = requests.get(siteMapURL, headers=headers)
        soup = BeautifulSoup(sitemap.text, "lxml")
        aTags = soup.find_all('loc')

        for aTag in aTags:
            href = aTag.text
            if href and siteIdentifier in href:
                urls.append(href)
    ranges = [0, 500, 1000, 2000, 3000, 5000, 7000, 10000, 50000]
    countRanges = [0]*len(ranges)

    totalWords, number_of_words, maxWords, minWords, maxUrl, minURL = 0, 0, 0, 9999999999, "", ""
    for i, url in enumerate(urls):
        print("", end="\r")
        print("Loading " + siteIdentifier + " blog post #", str(i), end="")
        title, text = get_text(url, contentClass)
        number_of_words = len(text.split())
        totalWords += number_of_words
        if maxWords < number_of_words:
            maxWords = number_of_words
            maxUrl = url
        if minWords > number_of_words:
            minWords = number_of_words
            minURL = url
        for i, upper in enumerate(ranges):
            if number_of_words < upper:
                countRanges[i] = countRanges[i] + 1
                break

    print("\n---" + siteIdentifier + "---")
    print("Total posts: " + str(len(urls)))
    for i in range(1, len(ranges)):
        print(str(ranges[i-1]) + "-" + str(ranges[i]) + ": " + str(countRanges[i]))
    print("Min words: " + str(minWords) + ", Max words: " + str(maxWords))
    print("Min Post: " + minURL + ", Max Post: " + maxUrl)
    print("Average post length: " + str(totalWords // len(urls)))
    print("Total post words: " + str(totalWords))
    print("")


getBlogStatistics(["https://jessenerio.com/post-sitemap.xml"], "jessenerio", 'elementor-widget-theme-post-content')
getBlogStatistics(["https://www.thesideblogger.com/post-sitemap.xml"], "thesideblogger", 'elementor-widget-theme-post-content')
getBlogStatistics(["https://fatstacksblog.com/post-sitemap1.xml", "https://fatstacksblog.com/post-sitemap2.xml",
                   "https://fatstacksblog.com/post-sitemap3.xml", "https://fatstacksblog.com/post-sitemap4.xml"],
                  "fatstacksblog", 'entry-content')
