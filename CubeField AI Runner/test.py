from PIL import ImageGrab
import time

def resize_image(image, resized_size):
    size = image.size
    if(size[0] > resized_size[0] and size[1] > resized_size[1]):
        ratio = (size[0]-resized_size[0])-(size[1]-resized_size[1])
        if(ratio > 0):
            new_width  = resized_size[0]
            new_height = new_width * size[1] / size[0]
        else:
            new_height = resized_size[1]
            new_width  = new_height * size[0] / size[1]
        #print(new_height,new_width)
        image = image.resize((int(new_width), int(new_height)))
    #image.show()
    return image
time.sleep(3)
img = resize_image(ImageGrab.grab().crop((540, 390, 1325, 885)), [157, 99])
img.show();
