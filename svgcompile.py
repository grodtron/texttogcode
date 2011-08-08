#!/usr/bin/python

from __future__ import division
from BeautifulSoup import BeautifulStoneSoup, Tag
from sys import argv
from math import ceil
import re

class SVG(object):
   def __init__(self, infile):
      infile = open(infile, "r")

      self._soup = BeautifulStoneSoup(infile.read(), selfClosingTags=["path", "rect", "metadata"])

      infile.close()

      metadata = self._soup.find("metadata")

      self.chrWidth = int(metadata["chrwidth"])
      self.chrHeight = int(metadata["chrheight"])
      self.hPadding = int(metadata["hpadding"]) 
      self.vPadding = int(metadata["vpadding"]) 
      self.cols = int(metadata["gridwidth"])
      self.scale = int(metadata["scale"])
      self.style = metadata["style"]

      self.rows = int(ceil(len(self._soup.findAll("char")) / self.cols))

      self.width = (self.chrWidth + self.hPadding) * self.cols
      self.width += self.hPadding
      self.width *= self.scale

      self.height = (self.chrHeight + self.vPadding) * self.rows
      self.height += self.vPadding
      self.height *= self.scale

   def outputData(self, outfile):

      outSoup = BeautifulStoneSoup("", selfClosingTags=["path"])
      outRoot = Tag(outSoup, "svg")
      outRoot["xmlns"] = "http://www.w3.org/2000/svg"
      outRoot["width"] = self.width
      outRoot["height"] = self.height
      outRoot["version"] = 1.1

      outSoup.insert(0, outRoot)


      for char in reversed(self._soup.findAll("char")):
         path = Tag(outSoup, "path")
         path["d"] = char["d"]
         path["style"] = self.style
         outRoot.insert(0, path)


      svg_header = "<?xml version=\"1.0\" standalone=\"no\"?>\n"
      svg_header += "<!DOCTYPE svg PUBLIC \"-//W3C//DTD SVG 1.1//EN\""
      svg_header += " \"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd\">\n"

      self.scaleAndGridAlphabet(outSoup)

      outfile = open(outfile, "w")

      outfile.write(svg_header +  outSoup.prettify())

      outfile.close()

   def scaleAndGridAlphabet(self, soup):
      row, col = 0, 0
      for i, path in enumerate(soup.findAll("path")):
         if(col >= self.cols):
            col = 0
            row += 1

         offX = col * (self.chrWidth + self.hPadding) + self.hPadding
         offY = row * (self.chrHeight + self.vPadding) + self.vPadding

         offX *= self.scale
         offY *= self.scale

         path["d"] = self.scaleAndOffsetData(path["d"], self.scale, offX, offY)
         col += 1
      

   def scaleAndOffsetData(self, data, scale, offX, offY):
      data = re.sub("\s+", " ", data).strip()
      outdata = ""
   
      for movement in re.findall("([A-Z]+)(( [0-9]+)+)", data):
         outdata += movement[0] + " "
         points = movement[1].strip().split(" ")
         for i, point in enumerate(points):
            point = scale * int(point)
            point += offY if i % 2 else offX
            outdata += str(point) + " "
   
      return outdata


def main(argv):
   infile = argv[0]
   outfile = argv[1]

   svg = SVG(infile)

   svg.outputData(outfile)

if __name__ == "__main__":
   main(argv[1:])
