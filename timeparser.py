import os

filename = 'job.7299011.7.out'

lineno = 0

def split_line(text):
    # split the text
    words = text.split()
    # for each word in the line:
    for word in words:

        # print the word
        print(words)

for line in reversed(open('log/'+filename).readlines()):
  #print line.rstrip()
  #print line
  words = line.split()
  print words
  lineno +=1
  if lineno > 5:
      break
