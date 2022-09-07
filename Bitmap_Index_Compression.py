#Robert Panerio
#CS 351 - Bitmap index and compression
#March 11, 2022

#creates the bitmap index of a given file
def create_index(input_file, output_path, sorted):
    outputFileName = input_file                                                 #holds the name of the ouput file for later use

    inputFile  = open(input_file, "r")                                          #open the input file with reading permission
    inputs = []
    for n in inputFile:
        inputs.append(n)                                                        #append every line as an element in the array

    if(sorted == True):                                                         #checks if the user wants the data file to be sorted or not
        inputs.sort()                                                           #sort the array
        outputFileName += "_sorted"                                             #append to the output file name

    outputFile = open(output_path + outputFileName, "w+")                       #open the output file with reading and writing permission. Plus create the file if does not exist
    outputFile.seek(0)                                                          #seek and truncate. Clears the file if contents exist. Helps when overwriting the same file over and over
    outputFile.truncate(0)

    for n in inputs:                                                            #reads per line in file
        strOutput = ""
        animal_kinds = ['cat', 'dog', 'turtle', 'bird']                         #array that stores the animals

        arr = n.split(',')                                                      #divide the entire string into substrings accoring the kind, age, and if adopted.
                                                                                #then store the strings in an arr
        for j in animal_kinds:                                                  #determines which animal then append to str
            strOutput += '1' if(j == arr[0]) else '0'

        flag = True
        for i in range(10, 101, 10):                                            #determines the age of the animal then append to str
            if(int(arr[1]) <= i and flag == True):
                strOutput += '1'
                flag = False
            else:
                strOutput += '0'

        strOutput += '01\n' if (arr[2][0: len(arr[2])-1] == 'False') else '10\n'#checks if the animal is adopted or not. [0: len(arr[2])-1] removes the new line at the end
        outputFile.write(strOutput)                                             #write the bitmap index in the new outputFile

    #closes the file pointers
    outputFile.close()
    inputFile.close()

def create_run_string(runType, runCount, word_size):
    binWordStr = bin(runCount)[2: len(bin(runCount))]                           #converts the integer into binary then removes the prefix "0b"

    typeCount = len(binWordStr)
    while(typeCount <= (word_size - 3)):                                        #pads the binary with zeros to fit with the (word size -2)
        binWordStr = "0" + binWordStr
        typeCount += 1

    binWordStr = "10" + binWordStr if (runType == "0") else "11" + binWordStr   #determines what type of runs
    return binWordStr

def compress_index(bitmap_index, output_path, compression_method, word_size):
    fileName = bitmap_index.split('/')
    outputFileName = fileName[len(fileName) - 1] + "_" + compression_method + "_" + str(word_size)

    file = open(bitmap_index, "r")
    outputFile = open(output_path + outputFileName, "w+")                       #open the output file with reading and writing permission. Plus create the file if does not exist
    outputFile.seek(0)                                                          #seek and truncate. Clears the file if contents exist. Helps when overwriting the same file over and over
    outputFile.truncate(0)

    if(compression_method == "WAH"):
        runType = "0"

        for i in range(0,16):                                                   #looping each character in a line from the file without including new line
            workingStr = ""
            runCount = 0
            charCount = 0
            file.seek(0)

            for lines in file:                                                  #looping each line in the file
                charCount += 1
                workingStr += lines[i]

                if(charCount == word_size - 1):                                  #to make sure that the bits are in the right word size
                    ifRun = len(set(workingStr))

                    if( ifRun == 1):                                            #if it is a run
                        if(runCount == pow(2, word_size -2) -1):                #if the compression can not handle more runs
                            outputFile.write(create_run_string(runType, runCount, word_size))
                            runCount = 0

                        elif(runType != workingStr[0] and runCount != 0):       #if the type of run changes proceed to appending the string to the file.
                            #e.g if a zero-typed run is followed with a one-typed run. Vice versa
                            outputFile.write(create_run_string(runType, runCount, word_size))
                            runCount = 0

                        runType = workingStr[0]                                 #reset the run type
                        runCount += 1

                    else:
                        if(runCount != 0 ):                                     #write the runs to the file. Only happens if a typed (zero or one) run is followed by a literal
                            outputFile.write(create_run_string(runType, runCount, word_size))
                            runCount = 0

                        outputFile.write("0" + workingStr)                      #if it is a literal

                    workingStr = ""
                    charCount = 0

            if(runCount != 0):                                                  #if the last bits are runs write to the file
                outputFile.write(create_run_string(runType, runCount, word_size))

            if(len(workingStr) != 0):                                           #if the last bits are less than (word size - 1)
                workingStr = "0" + workingStr                                   #make the last bits a literal
                padCount = len(workingStr)
                while(padCount < word_size):                                    #pad the last bits that is less than the (word size - 1)
                    workingStr = workingStr + "0"
                    padCount+=1
                outputFile.write(workingStr)                                    #write to the file

            outputFile.write('\n')

    #close the file pointers
    outputFile.close()
    file.close()

create_index('animals_sorted.txt','my_bitmaps/', False)
compress_index('my_bitmaps/animals_sorted.txt', 'my_compressed/animals_sorted/', 'WAH', 16)
