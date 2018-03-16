
import sqlite3

def writeTextFile(fileName, content):
    with open("output/" + fileName, "w") as f: 
        f.write(content)
    print(fileName, "written as text")

def writeBinaryFile(fileName, content):
    with open("output/" + fileName, "wb") as f: 
        f.write(content)
    print(fileName, "written as binary")

conn = sqlite3.connect('sergei.db')

cur = conn.cursor()
sql = """
SELECT es.title, e.raw, e.rawType
FROM entry e
INNER JOIN entrySearch es on es.entryFK = e.entryID 
order by e.entryID
"""
cur.execute(sql)

for row in cur:
    #print row
    title = str(row[0])
    rawType = int(row[2])
    fileName = title.replace('/', '-').replace(':', '-')

    if title.startswith('moved-') or title.startswith('mtgd-'):
        # print 'ignoring: ', title
        continue

    if rawType == 3:
        # markdown
        fileName += ".md"
        writeTextFile(fileName, str(row[1]))
    elif rawType == 1:
        # plain text
        fileName += ".txt"
        writeTextFile(fileName, str(row[1]))
    elif rawType == 4:
        # png - use current
        writeBinaryFile(fileName, row[1])
        pass
    else:
        print ("unknown rawType", rawType, title)
        continue

    #print (title, fileName )
    #fileName = title + "."
    #f = open()

conn.close()
