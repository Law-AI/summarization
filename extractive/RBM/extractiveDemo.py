from bs4 import BeautifulSoup
import os

def readPaths(path):
  # Create array of array of images.
  print(path)
  imagePaths = []
  filePaths = []
  # List all files in the directory and read points from text files one by one
  for filePath in sorted(os.listdir(path)):
    # print("10 ", filePath)
    fileExt = os.path.splitext(filePath)[1]
    if fileExt in [".html"]:
      # print (filePath)
      filePaths.append(filePath)

      # Add to array of images
      imagePaths.append(os.path.join(path, filePath))

  return imagePaths, filePaths

print('Enter directory for text files')
dirname2 = input()
for dirs in os.listdir(dirname2):
  if dirs in ['2013', '2014']:
	# print(type(dirs))
    if os.path.isdir(os.path.join(dirname2,dirs)):
      summaryFiles, names = readPaths(os.path.join(os.path.join(dirname2,dirs),'CaseAnalysis'))
      # print("hello")
      textFiles, names = readPaths(os.path.join(os.path.join(dirname2,dirs),'FullText'))
      # print(summaryFiles)
      # print(textFiles)
      for count in range(0,min(len(summaryFiles),len(textFiles))):
        HtmlFile = open(textFiles[count], 'r', encoding='utf-8')
        source_code = HtmlFile.read()
        soup = BeautifulSoup(source_code, 'html.parser')
        allDiv = soup.find_all('div', class_='locatorSection')
        #f = open("Summary_7.txt","wb")
        text = str()
        for i in allDiv:
            #print(i.find_all('h3'))
            flag = 0
            for h3tag in i.find_all('h3'):
                if h3tag.get('id') == 'casedigest':
                    flag = 1
                    break
            if flag == 1:
                for p in i.find_all('p'):
                    if p.find('strong') != None:
                        if p.find('strong').text == 'Summary:':
                            for tag in p.find_all('strong'):
                                tag.replaceWith('')
                            # print(p.text)
                            text = p.text
                            #f.write(bytes(text,'UTF-8'))

        #f.close()
        if any(os.path.basename(textFiles[count]) in  os.path.basename(s) for s in textFiles):
          HtmlFile = open(textFiles[count], 'r', encoding='utf-8')
          source_code = HtmlFile.read()
          soup = BeautifulSoup(source_code, 'html.parser')
          allDiv = soup.find_all('div', class_='docContent')

          f = open("Extractive/demo_test/"+dirs+"_"+names[count]+".txt","w")
          print("64 ", dirs+"_"+names[count])
          for i in allDiv:
              footNotes = i.find_all('p', class_='small center')
              for tag in footNotes:
                  tag.replaceWith('')
              # print(i.text)
              # f.write(i.text)
              # f.write("\n\n@highlight\n")
              f.write(text)

          f.close()
