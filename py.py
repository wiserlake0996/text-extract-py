import json

ios_data = []
gs4_data = []
win_data = []
droid_data = []
droid2_data = []

def extractIOS(ios_extract):

    ios_split_by_error = []
    ios_string = ""

    for i in range(len(ios_extract)):
        if ("HOW TO FIX" in ios_extract[i].upper() or "HOW TO IMPROVE" in ios_extract[i].upper()):
            ios_string += ios_extract[i] +"\n"
            for i2 in range(i+1,len(ios_extract)):
                if i2 == len(ios_extract):
                    ios_split_by_error.append(ios_string)
                    break

                if ("HOW TO FIX" in ios_extract[i2].upper() or "HOW TO IMPROVE" in ios_extract[i2].upper()):
                    ios_split_by_error.append(ios_string)
                    i = i2 - 1
                    ios_string = ""
                    break
                ios_string += ios_extract[i2] + "\n"

                
    return ios_split_by_error
        

    
def extractGS4(gs4_extract):
    gs4_split_by_error = []
    gs4_string = ""
    
    #check if 'PROBLEM:' exists in line to identify start of an error set"""
    for g in range(len(gs4_extract)):
        if("PROBLEM:" in gs4_extract[g].upper()):
            
            #add the header / error name to string
            gs4_string +=gs4_extract[g]+"\n"
            
            #Loop and add every other line to string till another error set is found"""
            for g2 in range(g+1, len(gs4_extract)):
                #if at the end, add the last item and exit
                if g2 == len(gs4_extract): 
                    gs4_split_by_error.append(gs4_string)
                    break
                    
                if ("PROBLEM:" in gs4_extract[g2].upper()):
                    gs4_split_by_error.append(gs4_string)
                    #re-focus pointer of outer loop to inner (loop -1) landing just before the next error set header
                    g= g2 - 1
                    gs4_string = ""
                    break
               
                gs4_string += gs4_extract[g2] + "\n"
            
    return gs4_split_by_error                         
    
           

def extractWIN(win_extract):
        
    win_split_by_error = []
    win_string = ""    
    
    #Check for header keywords on each line to identify start of error 
    for w in range(len(win_extract)):
        if("problem:" in win_extract[w].lower() or "bug:" in win_extract[w].lower() or "glitch:" in win_extract[w].lower() or "annoying:" in win_extract[w].lower()):
            
            win_string += win_extract[w] + "\n"
                        
            for w2 in range(w+1, len(win_extract)):
                if w2 == len(win_extract):
                    win_split_by_error.append(win_string)
                    break
                
                if("problem:" in win_extract[w2].lower() or "bug:" in win_extract[w2].lower() or "glitch:" in win_extract[w2].lower() or "annoying:" in win_extract[w2].lower()):
                    
                    win_split_by_error.append(win_string)
                    w= w2 - 1 
                    win_string = ""
                    break
                                
                win_string += win_extract[w2] + "\n"
    
    return win_split_by_error

    
"""************************************************************************"""

def extractDROID(droid_extract):
    droid_split_by_error = []
    droid_string = ""
    line_length = 7
    
    #check if 'PROBLEM:' exists in line to identify start of an error set"""
    for d in range(len(droid_extract)):
        
        line_length = len(droid_extract[d].split(' '))
        if(line_length < 6):
            
            #add the header / error name to string
            droid_string +=droid_extract[d]+"\n"
            
            #Loop and add every other line to string till another error set is found"""
            for d2 in range(d+1, len(droid_extract)):
                #if at the end, add the last item and exit
                if d2 == len(droid_extract): 
                    droid_split_by_error.append(droid_string)
                    break
                   
                line_length = len(droid_extract[d2].split(' '))
                if(line_length < 6):
                    droid_split_by_error.append(droid_string)
                    #re-focus pointer of outer loop to inner (loop -1) landing just before the next error set header
                    d= d2 - 1
                    droid_string = ""
                    break
               
                droid_string += droid_extract[d2] + "\n"
            
    return droid_split_by_error    
       
    
    
def extractDROID2(droid_extract2):
    ext = []
    
    ext.append(droid_extract2[0])
    ext.append(droid_extract2[1] )
    ext.append('\n'.join(droid_extract2[2:]))
        
    return ext     



def removeEmptyFromList(lst):
    return [line for line in lst if line.strip() != '']


def readFile():
    f = open("utf-errors.txt", "r")
    txt = f.read().splitlines()
    return txt

def splitFileIntoDevices(txt):
    split_store = []
    splits = ""
    count = 0
    for i in range(len(txt)):
        
        if len(txt[i].strip()) < 23 and (txt[i].strip().lower() == "IOS".lower() or txt[i].strip().lower() == "Android Problems".lower() or txt[i].strip().lower() == "GALAXY S4".lower() or txt[i].strip().lower() == "ANDROID USER ERRORS".lower() or txt[i].strip().lower() == "WINDOWS PHONE 8".lower()):
            #print "starting ", txt[i]
            for k in range(i+1,len(txt)):
                if k+1 == len(txt):
                    split_store.append(splits)
                    #print "total for ",txt[i] ,count
                    break

                if (txt[k].strip().lower() == "IOS".lower() or txt[k].strip().lower() == "Android Problems".lower() or txt[k].strip().lower() == "GALAXY S4".lower() or txt[k].strip().lower() == "ANDROID USER ERRORS".lower() or txt[k].strip().lower() == "WINDOWS PHONE 8".lower()):
                    split_store.append(splits)
                    i = k-1			
                    count = 0
                    splits = ""
                    break
                count+=1
                splits += txt[k] + "\n"    
    
    return split_store
    
    
def iosToDict():
    
    #list-dictionary or json array
    ios_list_dict = [{}] 
    
    count = 1
    for id in ios_data:
    
        #remove empty lines
        lines = removeEmptyFromList(id.split('\n'))
        
        #remove "HOW TO FIX and Description: keywords from bug data"
        lines[0] = lines[0].replace("HOW TO FIX ","")
        lines[1] = lines[1].replace("Description: ","")

        #Add data to list-dictionary
        tmp = {}
        tmp["id"] = "ios"+str(count)
        tmp["name"] = lines[0]
        tmp["description"] = lines[1] 
        tmp["body"] = '\n'.join(lines[2:])
        tmp["tag"] = "iphone, ios, ipad, apple"
        ios_list_dict.append(tmp)
        count = count + 1

    return json.dumps(ios_list_dict, separators=(',',':'), ensure_ascii=False)
    


def gs4ToDict():
    gs4_list_dict = [{}]
    count = 1
    for gd in gs4_data:
        lines = removeEmptyFromList(gd.split('\n'))
        
        lines[0] = lines[0].replace("PROBLEM: ","")
        tmp = {}
        tmp["id"] = "gs4"+str(count)        
        tmp["name"] = lines[0]
        tmp["description"] = lines[1] 
        tmp["body"] = '\n'.join(lines[2:])
        tmp["tag"] = "samsung, galaxy, s4, android"
        gs4_list_dict.append(tmp)
        count = count + 1
    
    return json.dumps(gs4_list_dict, separators=(',',':'), ensure_ascii=False)


def winToDict():
    win_list_dict = [{}]
    count = 1
    for wd in win_data:
        lines = removeEmptyFromList(wd.split('\n'))
        
        lines[0] = lines[0].lower().replace("bug: ","")
        lines[0] = lines[0].lower().replace("glitch: ","")
        lines[0] = lines[0].lower().replace("annoying: ","")
        lines[0] = lines[0].lower().replace("problem: ","")
        
        tmp = {}
        tmp["id"] = "win"+str(count)        
        tmp["name"] = lines[0]
        tmp["description"] = lines[1] 
        tmp["body"] = '\n'.join(lines[2:])
        tmp["tag"] = "windows, microsoft, windows phone"
        win_list_dict.append(tmp)
        count = count + 1
    
    return json.dumps(win_list_dict, separators=(',',':'), ensure_ascii=False)

def droidToDict():
    droid_list_dict = [{}]
    count = 1
    for dd in droid_data:
        lines = removeEmptyFromList(dd.split('\n'))
        tmp = {}
        tmp["id"] = "dd"+str(count)        
        tmp["name"] = lines[0]
        tmp["description"] = lines[1] 
        tmp["body"] = '\n'.join(lines[2:])
        tmp["tag"] = "android, droid"
        droid_list_dict.append(tmp)
        count = count + 1
    
    return json.dumps(droid_list_dict, separators=(',',':'), ensure_ascii=False)


def droid2ToDict():
    droid2_list_dict = [{}]
    
    count = 1
    lines = removeEmptyFromList(droid2_data)
    
    lines[0] = lines[0].lower().replace("1. ","")
    tmp = {}
    tmp["id"] = "ddd"+str(count)    
    tmp["name"] = lines[0]
    tmp["description"] = lines[1] 
    tmp["body"] = '\n'.join(lines[2:])
    tmp["tag"] = "android, droid"
    droid2_list_dict.append(tmp)
    count = count + 1
    
    return json.dumps(droid2_list_dict, separators=(',',':'), ensure_ascii=False)
    
def createJsonFile(fileData, fileName):
    the_file = open(fileName + '.json', 'w')
    the_file.truncate()
    the_file.write(fileData)
    the_file.close() 



def main():
    """read file, filter file by devices and filter devices by errors"""
    
    file_data = readFile()
    
    data_by_device = splitFileIntoDevices(file_data)
    
    
    ios_data.extend(extractIOS(removeEmptyFromList(data_by_device[0].split('\n'))))
    gs4_data.extend(extractGS4(removeEmptyFromList(data_by_device[1].split('\n'))))
    win_data.extend(extractWIN(removeEmptyFromList(data_by_device[2].split('\n'))))
    droid_data.extend(extractDROID(removeEmptyFromList(data_by_device[3].split('\n'))))
    droid2_data.extend(extractDROID2(removeEmptyFromList(data_by_device[4].split('\n'))))
    
    createJsonFile(iosToDict(), 'ios_bugs')
    createJsonFile(gs4ToDict(), 'gs4_bugs')
    createJsonFile(winToDict(), 'win_bugs')
    createJsonFile(droidToDict(), 'droid_bugs')
    createJsonFile(droid2ToDict(), 'droid2_bugs')
       

main()
