from .canvas_object import CanvasObject
from .util import combine_kwargs
import pdfkit 
from zipfile import ZipFile
import json
import os
import re

class File(CanvasObject):

   def get_file(self, file_id, **kwargs):
      """
      Return the standard attachment json object for a file.
      :calls: `GET /api/v1/files/:id \
      <https://canvas.instructure.com/doc/api/files.html#method.files.api_show>`_
      :rtype: dict
      """

      response = self._requester.request(
         "GET", "files/{}".format(file_id), _kwargs=combine_kwargs(**kwargs)
      )
      return response.json()

   def delete(self, file_id, **kwargs):
      """
      Delete this file.
      :calls: `DELETE /api/v1/files/:id  \
      <https://canvas.instructure.com/doc/api/files.html#method.files.destroy>`_
      :rtype: dict
      """
      response = self._requester.request(
         "DELETE", "files/{}".format(file_id), _kwargs=combine_kwargs(**kwargs)
      )
      return response.json()

   def download(self, file_url, location):
      """
      Download the file to specified location.
      :param location: The path to download to.
      :type location: str
      """
      response = self._requester.request("GET", _url=file_url)

      with open(location, "wb") as file_out:
         file_out.write(response.content)

   def get_contents(self, file_url, binary=False):
      """
      Download the contents of this file.
      Pass binary=True to return a bytes object instead of a str.
      :rtype: str or bytes
      """
      response = self._requester.request("GET", _url=file_url)
      if binary:
         return response.content
      else:
         return response.text
   
   # ------------------------------------------------------------------------------
   ### Author: by Pooja Pal 
   # ------------------------------------------------------------------------------  
   def generatePdfFile(self, syllabusPage):
      """
      Generates the PDf file to export syllabus page from the Canvas into PDF file
      :param syllabusPage: SyllabusPage dictionary contains course object, assignments object that together forms the Syllabus Page
      :type syllabusPage: dict
      :returns: pdf_file_name file name of the generated pdf 
      :rtype: string
      """
      if syllabusPage['course']['course_code'] is not None:
         html_file_name = "syllabus_" + syllabusPage['course']['course_code'] +"_"+ syllabusPage['course']['term']['name'] +".html"
      else:
         html_file_name = "syllabus.html"

      html_file_obj = open (html_file_name,'w')
      html_file_obj.write("<br>")
      html_file_obj.write("<h2>"+ syllabusPage['course']['name'] +" </h2><br>")
      html_file_obj.write("<h3> Term: "+ syllabusPage['course']['term']['name'] +" </h3><br>")
      html_file_obj.write("<h2> Course Syllabus </h2>")
      if syllabusPage['course']['syllabus_body'] is not None:
         with_anchor_tag = syllabusPage['course']['syllabus_body']
         without_anchor_tag = re.compile(r'<(?:a\b[^>]*>|/a>)').sub('', with_anchor_tag)
         html_file_obj.write(without_anchor_tag)
      html_file_obj.write("<style> td, th { border: 2px solid #dddddd;text-align: left;padding: 15px;} tr:nth-child(even) { background-color: #dddddd;}</style>")

      html_file_obj.write("<h2> Assignments </h2>")
      html_file_obj.write("<table><tr><th> Name</th><th>Due at <br>(yyyy-mm-dd)</th><th>Possible Points </th></tr>")
      for name, details in syllabusPage['assignments'].items():
         html_file_obj.write("<tr>")
         if details[0] is not  None:
               # html_file_obj.write("<td> <a href='"+ details[0] + "'>" + name +"</a></td>")
               html_file_obj.write("<td>" + name + "</td>")
         else:
               html_file_obj.write("<td></td>") 
         if details[1] is not  None:
               html_file_obj.write("<td>" + details[1] +"</td>") 
         else:
               html_file_obj.write("<td></td>") 
         if details[2] is not  None:
               html_file_obj.write(f"<td> {details[2]} </td>")
         else:
               html_file_obj.write("<td></td>") 
         html_file_obj.write("</tr>")
      html_file_obj.write("</table>")
      html_file_obj.close()

      pdf_file_name = html_file_name.replace(".html",".pdf")
      self.convertHtmlToPdf(html_file_name,pdf_file_name)
      return pdf_file_name

   def convertHtmlToPdf(self, html_file_name,pdf_file_name):
      """
      Serves as a helper function to convert HTML files to PDF file
      :param html_file_name: html file name 
      :type html_file_name: string
      :param pdf_file_name: PDF file name
      :type pdf_file_name: string
      :returns: None 
      """
      pdfkit.from_file(html_file_name,pdf_file_name)
      os.remove(html_file_name)

   def zipFiles(self,files):
      """
      zips the PDF file if if number of files is more than one.
      :param files: list of file names 
      :type files: List
      :returns: None 
      """
      with ZipFile('Syllabus.zip', 'w') as zipObj:
         for file in files:
            zipObj.write(file)
            os.remove(file)
      zipObj.close()
   