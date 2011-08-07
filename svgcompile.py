#!/usr/bin/python

from __future__ import division
from BeautifulSoup import BeautifulStoneSoup
from sys import argv
from math import ceil
import re

class SVG(object):
   def __init__(self, infile):
      infile = open(infile, "r")

      self._soup = BeautifulStoneSoup(infile.read(), selfClosingTags=["path", "rect"])

      infile.close()

      scale = self._soup.find("rect", {"id":"scale"})
      self.scale = int(scale["width"])
      scale.extract()

      grid = self._soup.find("rect", {"id":"grid"})
      self.cols = int(grid["width"])
      grid.extract()

      self.rows = int(ceil(len(self._soup.findAll("path")) / self.cols))

      ratio = self._soup.find("rect", {"id":"ratio"})
      self.chrWidth = int(ratio["width"])
      self.chrHeight = int(ratio["height"])
      ratio.extract()

      padding = self._soup.find("rect", {"id":"padding"})
      self.hPadding = int(padding["width"])
      self.vPadding = int(padding["height"])
      padding.extract()

      self.width = (self.chrWidth + self.hPadding) * self.cols
      self.width += self.hPadding
      self.width *= self.scale

      self.height = (self.chrHeight + self.vPadding) * self.rows
      self.height += self.vPadding
      self.height *= self.scale

      svg = self._soup.find("svg")
      svg["height"] = self.height
      svg["width"] = self.width

   def outputData(self, outfile):
      outfile = open(outfile, "w")

      outfile.write(self._soup.prettify())

      outfile.close()

   def scaleAndGridAlphabet(self):
      row, col = 0, 0
      for i, path in enumerate(self._soup.findAll("path")):
         if(col > self.cols):
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

   svg.scaleAndGridAlphabet()

   svg.outputData(outfile)

   #infile = open(infile, "r")
   #outfile = open(outfile, "w")
#
   #soup = BeautifulStoneSoup(infile.read(), selfClosingTags=["path", "rect"])
#
   #print repr(soup)
#
   #for i, path in enumerate(soup.findAll("path")):
      #path["d"] = scaleAndOffsetData(path["d"], 1, 3, 5)
   #


if __name__ == "__main__":
   main(argv[1:])
