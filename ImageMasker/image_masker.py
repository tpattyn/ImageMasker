import argparse, os, logging, cv2, sys
from PIL import Image, ImageDraw
from scipy import misc
import numpy as np
import ntpath

logger = logging.getLogger()

if __name__ == "__main__":

    parser  = argparse.ArgumentParser(description='Create a mask on images.')
    parser.add_argument('--c', action='store_true', default=False, help='Use a mask around the center of the image')
    parser.add_argument('--coordinates', required=True, metavar='px', type=int, nargs='+', help='Pixel coordinates for the mask')
    parser.add_argument('--images', required=True, metavar='IMG', type=str, nargs='+', help='Images to mask')

    args = parser.parse_args()

    #convert input image filenames to absolute path
    inputFiles = []
    for file in args.images:
        if os.path.isfile(file):
            if not os.path.isabs(file):
                file = os.path.join('/', os.getcwd(), file)
        else:
            logger.critical("%s Does not exist. Exiting", file)
        inputFiles.append(file)

    if not os.path.exists('Masked_images'):
        os.mkdir('Masked_images')


    for idx, imageFile in enumerate(inputFiles):
        print "Masking image " + str(idx)
        try:
            img = Image.open(imageFile)
            exif = img.info['exif']
            w, h = img.size
            center = (h/2, w/2)

            if args.c:
                mask = ((center[0] - args.coordinates[0], center[1] - args.coordinates[1]),
                        (center[0] + args.coordinates[0], center[1] + args.coordinates[1]))
            else:
                mask = ((args.coordinates[0], args.coordinates[2]),
                        (args.coordinates[1], args.coordinates[3]))

            draw = ImageDraw.Draw(img)
            draw.rectangle([(0,0), (w, mask[0][0])], fill=(0,0,0))
            draw.rectangle([(0, mask[1][0]), (w, h)], fill=(0,0,0))
            draw.rectangle([(0,mask[0][0]), (mask[0][1], mask[1][0])], fill=(0,0,0))
            draw.rectangle([(mask[1][1], mask[0][0]), (w, mask[1][0])], fill=(0,0,0))

            img.save("Masked_images/" + ntpath.basename(imageFile), exif=exif, quality=100)

        except IOError:
            logging.critical("Cannot read image file: $s" % imageFile)


    # for idx, imageFile in enumerate(inputFiles):
    #     try:
    #         img = cv2.imread(imageFile)
    #         x, y, _ = img.shape
    #         center = (x/2, y/2)
    #         mask = None
    #         if args.c:
    #             mask = ((center[0] - args.coordinates[0], center[1] - args.coordinates[1]),
    #                     (center[0] + args.coordinates[0], center[1] + args.coordinates[1]))
    #         else:
    #             mask = ((args.coordinates[0], args.coordinates[2]),
    #                     (args.coordinates[1], args.coordinates[3]))
    #         unmasked = img[mask[0][0]:mask[1][0], mask[0][1]:mask[1][1]].copy()
    #         img[:,:] = [0,0,0]
    #         img[mask[0][0]:mask[1][0], mask[0][1]:mask[1][1]] = unmasked
    #
    #         cv2.namedWindow(imageFile, cv2.WINDOW_NORMAL)
    #         cv2.imshow(imageFile, img)
    #         cv2.waitKey(0)
    #         cv2.destroyAllWindows()
    #
    #         cv2.imwrite("Masked_images/image" + str(idx) + ".jpg", img)
    #
    #
    #
    #     except IOError:
    #         logging.critical("Cannot read image file: %s" % imageFile)
