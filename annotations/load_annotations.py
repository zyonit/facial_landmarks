# This script translates the annotations from Superannotate software to the wflw format annotations
# it receives annotations.json and classes.json from the Superannotate export format.
# it outputs:
#   outputAnnotations.txt - coordinates of 98 landmarks (196) + coordinates of upper left corner and lower right corner of detection rectangle (x1, y1, x2, y2) (4) +  image name (1)
#   scripts.log - this log is helpful to debug errors in annotations.
#Notes
#   The script saves only images with all annotations (if an error was detected the images isn't saved to the text file).
# for future processing - better if image name doesnt include spaces.

# to execute this script
# change the annotations.json file to the correct one.
# delete scripts.log file (the script doesnt rewrite the log file, it continues it.)

import logging
import json
import datetime

# initialize the log settings
logging.basicConfig(filename=f'script_{datetime.datetime.now().strftime("%Y%m%d-%H%M%S")}.log',level=logging.INFO)

# Opening JSON file
f = open('src/annotations.json', )
c = open('src/classes.json', )

# returns JSON object as
# a dictionary
annotations = json.load(f)
classes_json = json.load(c)
f.close()
c.close()

#output text file
outF = open("src/outputAnnotations.txt", "w")

# new dictionary of only relevant information of classes maping
classes = {}
for key in classes_json:
    classes[key['id']] = {"name": key['name'] ,"attribute_groups" : key["attribute_groups"]  }

print(classes)
# Iterating through the json
# list
for imagename in annotations:

    tmp_image_annotation = [0.0,0.0]* 98
    tmp_image_bbox = []

    polygons_validation = 0 # used to count that the images have all the needed labels
    nose_validation = []
    nostrils_validation = []
    outlines_validation= []
    pupils_validation = 0
    bbox_validation =0
    for label_dic in annotations[imagename]:
        try:
            if label_dic["type"] == "meta": # all images have a 'meta' type label, with no important information, therefore ignore
                continue
            if classes[label_dic['classId']]['name'] == 'lefteyebrow':
                try:
                    assert(len(label_dic['points'])==18)
                    tmp_image_annotation[42*2:42*2+18] = label_dic['points']
                    print(type(label_dic['points'][0]))

                    polygons_validation +=1
                    logging.info(f'Image {imagename}: updated {classes[label_dic["classId"]]["name"]}')
                except Exception  as e:
                    print(f'Image {imagename}: wrong number of points in {classes[label_dic["classId"]]["name"]} polygon ')
                    logging.error(f'Image {imagename}: wrong number of points in {classes[label_dic["classId"]]["name"]} polygon ')
                    continue

            if classes[label_dic['classId']]['name'] == 'lefteye':
                try:
                    assert(len(label_dic['points'])==16)
                    tmp_image_annotation[68*2:68*2+16] = label_dic['points']
                    polygons_validation +=1
                    logging.info(f'Image {imagename}: updated {classes[label_dic["classId"]]["name"]}')
                except Exception  as e:
                    print(f'Image {imagename}: wrong number of points in {classes[label_dic["classId"]]["name"]} polygon ')
                    logging.error(f'Image {imagename}: wrong number of points in {classes[label_dic["classId"]]["name"]} polygon ')
                    continue


            if classes[label_dic['classId']]['name'] == 'righteyebrow':
                try:
                    assert(len(label_dic['points'])==18)
                    tmp_image_annotation[33*2:33*2+18] = label_dic['points']
                    polygons_validation +=1
                    logging.info(f'Image {imagename}: updated {classes[label_dic["classId"]]["name"]}')
                except Exception  as e:
                    print(f'Image {imagename}: wrong number of points in {classes[label_dic["classId"]]["name"]} polygon ')
                    logging.error(f'Image {imagename}: wrong number of points in {classes[label_dic["classId"]]["name"]} polygon ')
                    continue

            if classes[label_dic['classId']]['name'] == 'righteye':
                try:
                    assert(len(label_dic['points'])==16)
                    tmp_image_annotation[60*2:60*2+16] = label_dic['points']
                    polygons_validation +=1
                    logging.info(f'Image {imagename}: updated {classes[label_dic["classId"]]["name"]}')
                except Exception  as e:
                    print(f'Image {imagename}: wrong number of points in {classes[label_dic["classId"]]["name"]} polygon ')
                    logging.error(f'Image {imagename}: wrong number of points in {classes[label_dic["classId"]]["name"]} polygon ')
                    continue

            if classes[label_dic['classId']]['name'] == 'outerlips':
                try:
                    assert(len(label_dic['points'])==24)
                    tmp_image_annotation[76*2:76*2+24] = label_dic['points']
                    polygons_validation +=1
                    logging.info(f'Image {imagename}: updated {classes[label_dic["classId"]]["name"]}')
                except Exception  as e:
                    print(f'Image {imagename}: wrong number of points in {classes[label_dic["classId"]]["name"]} polygon ')
                    logging.error(f'Image {imagename}: wrong number of points in {classes[label_dic["classId"]]["name"]} polygon ')
                    continue

            if classes[label_dic['classId']]['name'] == 'innerlips':
                try:
                    assert (len(label_dic['points']) == 16)
                    tmp_image_annotation[88 * 2:88 * 2 + 16] = label_dic['points']
                    polygons_validation += 1
                    logging.info(f'Image {imagename}: updated {classes[label_dic["classId"]]["name"]}')
                except Exception  as e:
                    print(f'Image {imagename}: wrong number of points in {classes[label_dic["classId"]]["name"]} polygon ')
                    logging.error(
                        f'Image {imagename}: wrong number of points in {classes[label_dic["classId"]]["name"]} polygon ')
                    continue

            if classes[label_dic['classId']]['name'] == 'face_boundingbox':
                try:
                    tmp_image_bbox = [int(label_dic['points']['x1']) , int(label_dic['points']['y1']), int(label_dic['points']['x2']),int(label_dic['points']['y2'])]
                    ##fill outline with a landmark inside the face crop
                    tmp_image_annotation[0:33*2] = [label_dic['points']['x1'] , label_dic['points']['y1']] *33
                    logging.info(f'Image {imagename}: updated {classes[label_dic["classId"]]["name"]}')
                    bbox_validation +=1
                except Exception  as e:
                    print(f'Image {imagename}: error in {classes[label_dic["classId"]]["name"]}' )
                    logging.error(f'Image {imagename}: error in {classes[label_dic["classId"]]["name"]} ')
                    continue

            if classes[label_dic['classId']]['name'] == 'nose':
                try:
                    x = label_dic['x']
                    y = label_dic['y']
                    id = label_dic['attributes'][0]['id']
                    index = int(next((item for item in classes[label_dic['classId']]['attribute_groups'][0]['attributes'] if item['id'] == id), "Default value")['name'])
                    nose_validation.append(index)
                    tmp_image_annotation[index*2:index*2+2] = [x , y]
                    logging.info(f'Image {imagename}: updated point {index}')
                except Exception  as e:
                    print (f'Image {imagename}: could not calculate  {classes[label_dic["classId"]]["name"]} point, Error occurred : ' + str(e))
                    logging.error(f'Image {imagename}: could not calculate  {classes[label_dic["classId"]]["name"]}  point, Error occurred : ' + str(e))
                    continue

            if classes[label_dic['classId']]['name'] == 'outlines':
                try:
                    x = label_dic['x']
                    y = label_dic['y']
                    id = label_dic['attributes'][0]['id']
                    index = int(next((item for item in classes[label_dic['classId']]['attribute_groups'][0]['attributes'] if item['id'] == id), "Default value")['name'])
                    outlines_validation.append(index)
                    tmp_image_annotation[index*2:index*2+2] = [x , y]
                    logging.info(f'Image {imagename}: updated point {index}')
                except Exception  as e:
                    print (f'Image {imagename}: could not calculate  {classes[label_dic["classId"]]["name"]} point, Error occurred : ' + str(e))
                    logging.error(f'Image {imagename}: could not calculate  {classes[label_dic["classId"]]["name"]}  point, Error occurred : ' + str(e))
                    continue

            if classes[label_dic['classId']]['name'] == 'nostrils':
                try:
                    x = label_dic['x']
                    y = label_dic['y']
                    id = label_dic['attributes'][0]['id']
                    index = int(next((item for item in classes[label_dic['classId']]['attribute_groups'][0]['attributes'] if item['id'] == id), "Default value")['name'])
                    tmp_image_annotation[index*2:index*2+2] = [x , y]
                    nostrils_validation.append(index)
                    logging.info(f'Image {imagename}: updated point {index}')
                except Exception  as e:
                    print (f'Image {imagename}: could not calculate  {classes[label_dic["classId"]]["name"]} point, Error occurred : ' + str(e))
                    logging.error(f'Image {imagename}: could not calculate  {classes[label_dic["classId"]]["name"]}  point, Error occurred : ' + str(e))
                    continue

            if classes[label_dic['classId']]['name'] == 'leftpupil':
                try:
                    x = label_dic['x']
                    y = label_dic['y']
                    tmp_image_annotation[194:196] = [x , y]
                    pupils_validation +=1
                    logging.info(f'Image {imagename}: updated  leftpupil point')
                except Exception  as e:
                    print (f'Image {imagename}: could not calculate  {classes[label_dic["classId"]]["name"]} point, Error occurred : ' + str(e))
                    logging.error(f'Image {imagename}: could not calculate  {classes[label_dic["classId"]]["name"]}  point, Error occurred : ' + str(e))
                    continue
            if classes[label_dic['classId']]['name'] == 'rightpupil':
                try:
                    x = label_dic['x']
                    y = label_dic['y']
                    tmp_image_annotation[192:194] = [x , y]
                    pupils_validation +=1
                    logging.info(f'Image {imagename}: updated rightpupil point ')
                except Exception  as e:
                    print (f'Image {imagename}: could not calculate  {classes[label_dic["classId"]]["name"]} point, Error occurred : ' + str(e))
                    logging.error(f'Image {imagename}: could not calculate  {classes[label_dic["classId"]]["name"]}  point, Error occurred : ' + str(e))
        except Exception  as e:
            print(f'Image {imagename}: Error occurred : ' + str(e))
            logging.error(f'Image {imagename}: Error occurred : ' + str(e))
    # make sure we have all the annotations
    try:
        assert(bbox_validation == 1)
    except:
        print( f'Image {imagename}: missing bbox')
        logging.error( f'Image {imagename}: missing bbox')

    try:
        assert(len(set(nostrils_validation)) == 5)

    except:
        print( f'Image {imagename}: wrong number of nostrils points')
        logging.error( f'Image {imagename}: wrong number of nostrils points')

    try:
        assert (len(set(nose_validation)) == 4)

    except:
        print(f'Image {imagename}:  wrong number of nose points')
        logging.error(f'Image {imagename}:  wrong number of nose points')
    try:
        assert (len(set(outlines_validation)) == 33)

    except:
        print(f'Image {imagename}:  wrong number of outlines points')
        logging.error(f'Image {imagename}:  wrong number of outlines points')


    try:
        assert (pupils_validation == 2)
    except:
        print(f'Image {imagename}: missing pupil points')
        logging.error(f'Image {imagename}: missing pupil points')

    try:
        assert ((pupils_validation+ polygons_validation +len(set(nose_validation)) + len(set(nostrils_validation))+ bbox_validation+ len(set(outlines_validation))  == 51))
        logging.info(f"Image {imagename}: verified all annotations exist. Ready to write")
        outF.write(str(tmp_image_annotation + tmp_image_bbox).replace(',', '')[1:-1]+ " " + imagename)
        str(tmp_image_annotation + tmp_image_bbox).replace(',', '')[1:-1]+ " " + imagename
        #str(tmp_image_annotation + tmp_image_bbox)
        outF.write("\n")
    except:
        print(f'Image {imagename}: missing some labels, skipping image')
        logging.error(f'Image {imagename}: missing some label, skipping image')





outF.close()

