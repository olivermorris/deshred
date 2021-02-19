words= []
# this opens the text file that contains a english lanuage dictionary
with open("words.txt") as data:
    datalines = (line.rstrip('\r\n') for line in data)
    for line in datalines:
         words.append(line.lower())
# these are test shreds in a list of lists. Each list represents the words you kight find on a shred
shreds = [
    ["futu","for","ngth","re su","d st","ce a","ecial","rms book"],
    ["re price","each in","of your","bject to,","nding a","portion","discount","f service"]
] 
for shred in shreds:
    for word in shred:
        print(word)
# defines a pivot point IE a shred that doesent move. The other shreds are tested around it   
pivot = shreds[1]
compare = []
compare2 = []
wordi = []
scorenum = 0
class Swap:
  def __init__(self, pivot, point):
    self.pivot = pivot
    self.point = point
  def langcheck(self):
    length = 0
    #print(self.pivot)
    for thing in self.pivot:
         loc = (self.pivot.index(thing))
         print("space")
         combination = (thing+self.point[loc])
         print(combination)
         scorestr = combination.split()
         print(scorestr,"123")
         for scoree in scorestr:
            try:
                words.index(scoree)
                print(scoree,"scoree")
                length += ((len(scoree)**2))
                print(length,"this is the current lenhth")
            except:
                   print(scoree,"This failed")
                   print(len(scoree))
                   length -= (len(scoree))
                   print(length)
    if length > 0:
        print("This is a correct order")
    else:
        print("This order is incorrect")
                   
        
                    
            
                    
# toggle these to affect the pivot point                    
x = Swap(shreds[0],shreds[1])

x.langcheck()
print(length,"This is the length")
