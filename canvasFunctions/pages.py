import pypandoc
import os

#----------------------------------------------------------------------------
# Function to return the HTML and content of the specific canvas page as 
# a html page(canvasPage.html)
def getFileContent(page, fileType):
   dirtyString = page.get('body')
   fileName = page.get('title')
   f = open("canvasPage.html", "x")
   f.write(dirtyString)
   f.close()

   if fileType == 'docx':
      fileName = fileName + ".docx"
      pypandoc.convert_file('canvasPage.html', 'docx',
                           outputfile=(fileName))

   os.remove("canvasPage.html")
   
   return fileName