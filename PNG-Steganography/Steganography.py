from PIL import Image
import numpy as np
import sys
from os import path



def LoadImage (filePath : str) -> tuple[Image.Image, int, int]:

    with open(filePath, "rb") as file :
        if file.read(4) != b"\x89PNG" :
            print("only png files are supported")
            exit()

    if not path.exists(filePath):
        print ("image file not found")
        exit()
    
    image = Image.open(filePath, "r")
    width, height = image.size
    image = np.array(list(image.convert('RGBA').getdata()))

    return (image, width, height)



def MessageToBinary(messageFilePath : str) -> np.ndarray:

    if not path.exists(messageFilePath):
        print ("message file not found")
        exit()

    EndOfMessageFlag = b"$NIRLEKA$"
    with open(messageFilePath, "rb") as file :
        message = bytearray(file.read())
        message.extend(EndOfMessageFlag) 

    return np.frombuffer(message, dtype=np.uint8)



def InsertMessageToImage (imageData : np.ndarray , messageData : np.ndarray) -> np.ndarray :

    #satu pixel bisa memuat 1 byte data
    imagePixels = len(imageData)
    messageLength = (len(messageData))


    if imagePixels >= messageLength:

        imageData[:messageLength, 0] = (imageData[:messageLength, 0] & 0xfc) | ((messageData[:] >> 6) & 0x03)
        imageData[:messageLength, 1] = (imageData[:messageLength, 1] & 0xfc) | ((messageData[:] >> 4) & 0x03)
        imageData[:messageLength, 2] = (imageData[:messageLength, 2] & 0xfc) | ((messageData[:] >> 2) & 0x03)
        imageData[:messageLength, 3] = (imageData[:messageLength, 3] & 0xfc) | (messageData [:] & 0x03)

        return imageData

    else :

        print ("not enough space for the message")
        return



def SaveProcessedImage(processedImage : np.ndarray, width : int, height : int, filePath : str):

    processedImage = processedImage.reshape((height, width, 4))
    image = Image.fromarray(processedImage.astype("uint8"), "RGBA")
    image.save(filePath)

    print ("selesai")



def ExtractMessageFromImage (imageData : np.ndarray, outputFile : str) -> None :

    fileBaseName = path.basename(outputFile)
    directoryPath = outputFile.replace(fileBaseName, "")
    directoryPath = "." if directoryPath == "" else directoryPath

    if not path.exists(directoryPath):
        print ("output directory not found")
        exit()

    imagePixels = len (imageData)

    extractedData = bytearray(imagePixels)
    extractedData = np.frombuffer(extractedData, dtype=np.uint8)

    extractedData[:] = extractedData[:] |\
                       ((imageData[:, 0] & 0x03) << 6) |\
                       ((imageData[:, 1] & 0x03) << 4) |\
                       ((imageData[:, 2] & 0x03) << 2) |\
                       ( imageData[:, 3] & 0x03) 

    extractedData = extractedData.tobytes()
    endOfMessageFlag = b"$NIRLEKA$"

    endOfMessageIndex = extractedData.find(endOfMessageFlag)
    extractedData = extractedData[:endOfMessageIndex]

    with open (outputFile, "wb") as file:
        dataBytes = extractedData
        file.write(dataBytes)
    
    print ("success")
    return 



def _Main_InsertImage(imageFilePath : str, messageFilePath : str, outputPath : str, *args : list[str]) -> None :
    
    imageData, width, height = LoadImage(imageFilePath)
    messageData = MessageToBinary(messageFilePath)

    processedImage = InsertMessageToImage(imageData, messageData)
    SaveProcessedImage(processedImage, width, height, outputPath)



def _Main_ExtractData(imageFilePath : str, outputPath : str, *args : list[str]) -> None :

    imageData = LoadImage(imageFilePath)[0]
    ExtractMessageFromImage(imageData, outputPath)



def ProcessData (argv : list[str]) -> None:

    mode = argv[0]
    if mode == "insert":
        _Main_InsertImage(*(argv[1:]))
    elif mode == "extract":
        _Main_ExtractData(*(argv[1:]))
    else :
        print ("unknown processing mode")



if __name__ == "__main__":

    argv = sys.argv

    if len(argv) > 2 :
        ProcessData(argv[1:])
    else : 
        errorMessage = "The syntax must be \
                        [mode : insert/ extract] [imagePath] \
                        [outputPath (for extract), messageFilePath (for insert)] \
                        [newImagePath (for insert)]"
        print (errorMessage)

    
