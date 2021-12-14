import os
from PIL import Image, ImageDraw
import numpy as np
import random
import re

# x, y
testSize = (500,500)
# y, x, because numpy.
desiredLayout = (5,5)
baseImagePath = "baseImage.png"

"""
piece naming system:
1 - unedited
2 - flat side
3 - intrusion
4 - protrusion
5 - error

"""

# prolly dont need idk.
def createAllFolders(filepath):
    if "\\" in filepath:
        only_folders = re.search(r".*(?=\\)", filepath).group()

        if not os.path.exists(only_folders):
            if "\\" not in only_folders:
                current_folder = only_folders
                if not os.path.exists(current_folder):
                    os.mkdir(current_folder)

            else:
                all_folders = re.findall(r'^.*?(?=\\)|(?<=\\).*?(?=\\)|(?<=\\).+$',only_folders)
                current_folder = only_folders

                for folder in all_folders:
                    current_folder = os.path.join(current_folder,folder)
                    if not os.path.exists(current_folder):
                        os.mkdir(current_folder)

def oppSide(side):
    try:
        return [2,3,0,1][int(side)]
    except Exception as e:
        print(e)
        return 0

def neighbour(pos, i):
    """
    gives coord of neighbour based on direction
    """
    if int(i) == 0:
        return (pos[0], pos[1]-1)
    elif int(i) == 1:
        return (pos[0]+1, pos[1])
    elif int(i) == 2:
        return (pos[0], pos[1]+1)
    elif int(i) == 3:
        return (pos[0]-1, pos[1])
    else:
        return (0,0)

def generatePuzzle(pcs):
    """
    pcs is a tuple (y, x)
    """

    pL = np.full(shape=(pcs[0],pcs[1],4), fill_value=1, dtype=int)

    for y, row in enumerate(pL):
        for x, pc in enumerate(row):
            # print("Piece ({},{})".format(x,y))

            for i in range(4):
                oS = oppSide(i)
                nPC = neighbour((x, y), i)
                # print(nPC)

                # # edge check
                if nPC[0] == -1 or nPC[1] == -1 or nPC[0] == pcs[1] or nPC[1] == pcs[0]:
                    pc[i] = 2
                else:
                    if pL[nPC[1]][nPC[0]][oS] == 1:
                        pc[i] = random.randint(3,4)
                    elif pL[nPC[1]][nPC[0]][oS] == 2:
                        pc[i] = 2
                    elif pL[nPC[1]][nPC[0]][oS] == 3:
                        pc[i] = 4
                    elif pL[nPC[1]][nPC[0]][oS] == 4:
                        pc[i] = 3

                # print(oS, nPC, pcList)

            def oldCode():
                pass
                # # check up
                # if y == 0:
                #     # print("Top pc")
                #     pcList[0] = 2
                # # elif pL[x][y+1][0] == 0:
                # #     pL[x][y] = random.randint(2,3)
                # # elif pL[x][y+1][0] == 2:
                # #     pL[x][y] = 3
                # # elif pL[x][y+1][0] == 3:
                # #     pL[x][y] = 2
                # # else:
                # #     pL[x][y] = 4 # error

                # # check right
                # if x == pcs[1]-1:
                #     # print("Right pc")
                #     pcList[1] = 2

                # # check down
                # if y == pcs[1]-1:
                #     # print("Bottom pc")
                #     pcList[2] = 2

                # # check left
                # if x == 0:
                #     # print("Left pc")       
                #     pcList[3] = 2

            # print(foo)
            pL[y][x] = pc

    print(pL)

    return pL

def createPiece(
    baseImage,
    pcCode=4343, 
    pcCoord=(2,2),
    maxSize=testSize,
    rectSize=(100,100),
    circleDiameter=50,
    ):

    ### VARS AND STUFF
    emptyColor = (0,0,0,0)
    fillColor = (255,255,255,255)

    x0 = pcCoord[0] * rectSize[0]
    y0 = pcCoord[1] * rectSize[1]

    w = rectSize[0] - 1 #
    h = rectSize[1] - 1 #
    cD = circleDiameter - 1 #
    cR = int(cD / 2)
    wGap = int(((w - cD) / 2))
    hGap = int(((h - cD) / 2))

    # pillow.

    im = Image.new("RGBA", maxSize, emptyColor)
    draw = ImageDraw.Draw(im)

    # generate coord tuples.
    sqCoord = (x0, 
    y0, 
    x0 + w, 
    y0 +w)
    crCoords = [(x0 + 
    wGap, 
    y0 - cR, 
    x0 + wGap + cD, 
    y0 - cR + cD),
    (x0 + w - cR, 
    y0 + hGap, 
    x0 + w - cR + cD, 
    y0 + hGap + cD),
    (x0 + wGap, 
    y0 + h - cR, 
    x0 + wGap + cD, 
    y0 + h - cR + cD),
    (x0 - cR, 
    y0 + hGap, 
    x0 - cR + cD, 
    y0 + hGap + cD)]

    # create square
    draw.rectangle(
        sqCoord,
        fill=fillColor
    )

    # the circles:
    for i in range(4):
        side = pcCode[i]
        if side == 3:
            draw.ellipse(crCoords[i], fill=emptyColor)
        elif side == 4:
            draw.ellipse(crCoords[i], fill=fillColor)

    # overlaying base image
    finalPiece = baseImage.copy()
    finalPiece.putalpha(im.convert(mode="L"))

    fName = "Piece ({},{}).png".format(pcCoord[0], pcCoord[1])
    if not os.path.exists("Export Pieces"):
        os.mkdir("Export Pieces")
    finalPiece.save(os.path.join("Export Pieces", fName))

def main():
    print("Generating Puzzle Layout.")
    layout = generatePuzzle(desiredLayout)
    
    # base image, prefably of the correct size.
    baseImage = Image.open(baseImagePath)
    print("Loading Test Image: {}.".format(baseImagePath))

    for y, row in enumerate(layout):
        for x, pc in enumerate(row):
            print("Creating Piece ({},{}).".format(x, y))

            createPiece(
                baseImage=baseImage,
                pcCode=pc, 
                pcCoord=(x,y),
                maxSize=testSize,
                rectSize=(100,100),
                circleDiameter=50
                )

if __name__ == "__main__":
    main()
    input("Press enter to close.")