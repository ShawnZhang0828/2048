def listRecover(aList):
    recoveredList = []
    stringForCombine = ""
    for item in aList:
        if item.isnumeric() == True or item == ".":
            stringForCombine += item
        else:
            if stringForCombine != "":
                recoveredList.append(stringForCombine)
            stringForCombine = ""
    for i,num in enumerate(recoveredList):
        if "." in num:
            recoveredList[i] = float(num)
        else:
            recoveredList[i] = int(num)
    return recoveredList

f = open("record.txt", "r")
lines = f.readlines()
print (listRecover(lines[4]))

f.close()
