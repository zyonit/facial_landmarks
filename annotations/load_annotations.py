# Python program to read
# json file

# This scripts assumes:
# all images have no spaces in image name


import logging
import json

# initialize the log settings
logging.basicConfig(filename='script.log',level=logging.INFO)

# Opening JSON file
f = open('src/annotations.json', )
c = open('src/classes.json',)

# returns JSON object as
# a dictionary
annotations = json.load(f)
classes_json = json.load(c)
f.close()
c.close()

#output text file
outF = open("outputAnnotations.txt", "w")

# new dictionary of only relevant information of classes maping
classes = {}
for key in classes_json:
    classes[key['id']] = {"name": key['name'] ,"attribute_groups" : key["attribute_groups"]  }

# Iterating through the json
# list
for imagename in annotations:

    tmp_image_annotation = [0.0,0.0]* 98
    tmp_image_bbox = []

    polygons_validation = 0 # used to count that the images have all the needed labels
    nose_validation = []
    nostrils_validation = []
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
                    tmp_image_bbox = [label_dic['points']['x1'] , label_dic['points']['y1'], label_dic['points']['x2'],label_dic['points']['y2']]
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
        assert (pupils_validation == 2)
    except:
        print(f'Image {imagename}: missing pupil points')
        logging.error(f'Image {imagename}: missing pupil points')

    try:
        assert ((pupils_validation+ polygons_validation +len(set(nose_validation)) + len(set(nostrils_validation))+ bbox_validation)  == 18)
        logging.info(f"Image {imagename}: verified all annotations exist. Ready to write")
        outF.write(str(tmp_image_annotation + tmp_image_bbox).replace(',', '')[1:-1]+ " " + imagename)
        str(tmp_image_annotation + tmp_image_bbox).replace(',', '')[1:-1]+ " " + imagename
        #str(tmp_image_annotation + tmp_image_bbox)
        outF.write("\n")
    except:
        print(f'Image {imagename}: missing some labels, skipping image')
        logging.error(f'Image {imagename}: missing some label, skipping image')




outF.close()

# ###
# def addNumbers(a, b):
#     try:
#         return a + b
#     except Exception as e:
#         return 'Error occurred : ' + str(e)
#
#
# print
# addNumbers('', 10)