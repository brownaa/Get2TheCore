# https://stackoverflow.com/a/25307981/2142315
def LineIterator(P1, P2, img):
    """
    Produces and array that consists of the coordinates and intensities of each pixel in a line between two points

    Parameters:
        -P1: a numpy array that consists of the coordinate of the first point (x,y)
        -P2: a numpy array that consists of the coordinate of the second point (x,y)
        -img: the image being processed

    Returns:
        -it: a numpy array that consists of the coordinates and intensities of each pixel in the radii (shape: [numPixels, 3], row = [x,y,intensity])     
    """
    #define local variables for readability
    imageH = img.shape[0]
    imageW = img.shape[1]
    x1 = P1[0]   # P1X =
    y1 = P1[1]   # P1Y = 
    x2 = P2[0]   # P2X = 
    y2 = P2[1]   # P2Y = 

    #difference and absolute difference between points
    #used to calculate slope and relative location between points
    dX = x2 - x1
    dY = y2 - y1
    dXa = np.abs(dX)
    dYa = np.abs(dY)

    #predefine numpy array for output based on distance between points
    itbuffer = np.empty(shape=(np.maximum(dYa,dXa),3),dtype=np.float32)
    itbuffer.fill(np.nan)

    #Obtain coordinates along the line using a form of Bresenham's algorithm
    negY = y1 > y2
    negX = x1 > x2
    if x1 == x2: #vertical line segment
        itbuffer[:,0] = x1
        if negY:
            itbuffer[:,1] = np.arange(y1 - 1,y1 - dYa - 1,-1)
        else:
            itbuffer[:,1] = np.arange(y1+1,y1+dYa+1)              
    elif y1 == y2: #horizontal line segment
        itbuffer[:,1] = y1
        if negX:
            itbuffer[:,0] = np.arange(x1-1,x1-dXa-1,-1)
        else:
            itbuffer[:,0] = np.arange(x1+1,x1+dXa+1)
    else: #diagonal line segment
        steepSlope = dYa > dXa
        if steepSlope:
            slope = dX.astype(np.float32)/dY.astype(np.float32)
            if negY:
                itbuffer[:,1] = np.arange(y1-1,y1-dYa-1,-1)
            else:
                itbuffer[:,1] = np.arange(y1+1,y1+dYa+1)
            itbuffer[:,0] = (slope*(itbuffer[:,1]-y1)).astype(np.int) + x1
        else:
            slope = dY.astype(np.float32)/dX.astype(np.float32)
            if negX:
                itbuffer[:,0] = np.arange(x1-1,x1-dXa-1,-1)
            else:
                itbuffer[:,0] = np.arange(x1+1,x1+dXa+1)
            itbuffer[:,1] = (slope*(itbuffer[:,0]-x1)).astype(np.int) + y1

    #Remove points outside of image
    colX = itbuffer[:,0]
    colY = itbuffer[:,1]
    itbuffer = itbuffer[(colX >= 0) & (colY >=0) & (colX<imageW) & (colY<imageH)]

    #Get intensities from img ndarray
    itbuffer[:,2] = img[itbuffer[:,1].astype(np.uint),itbuffer[:,0].astype(np.uint)] 

    return itbuffer