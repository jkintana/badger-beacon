import requests, re, json
from bs4 import BeautifulSoup
from unidecode import unidecode

res = requests.get('https://www.wisc.edu/academics/majors/')
soup = BeautifulSoup(res.content, 'html5lib', from_encoding='utf-8')
nameRegex = re.compile('(?<=\<h3\>)(.*)(?= \<span\>)') # Get strings between <h3> and <span>
descriptionRegex = re.compile('(?<=\>)(.*)(?=\<span)') # Get strings between > and <span
degreeList = {}

def cleanupString(toClean):
  toClean = unidecode(toClean)
  toClean = toClean.replace('&amp;', '&')
  toClean = toClean.strip()
  return toClean

for element in soup.select('.uw-major'):
  degreeType = element.get('data-degree') # BS, BA, Certificate, etc.

  degreeName = nameRegex.search(str(element.h3)).group() # Accounting, Zoology, etc.
  degreeName = cleanupString(degreeName)

  descriptionElement = str(element.select('.uw-major-text')) # Description of degree.
  degreeDescription = descriptionRegex.search(descriptionElement).group()
  degreeDescription = cleanupString(degreeDescription)

  if(degreeName not in degreeList.keys()):
    degreeList[degreeName] = {
      'degree_types' : [degreeType],
      'descriptions' : [degreeDescription]
    }
  else:
    currentDegree = degreeList[degreeName]
    currentDegree['degree_types'].append(degreeType)
    if(degreeDescription not in currentDegree['descriptions']):
      currentDegree['descriptions'].append(degreeDescription)

outputFile = open('./scraping/degreeInfo.json', 'w')
outputFile.write(json.dumps(degreeList))
outputFile.close()