

import numpy as np
import cv2
# from moviepy.editor import VideoFileClip
import face_recognition
# get_ipython().run_line_magic('matplotlib', 'inline')


# ## 3. Config &  init

# In[2]:


global global_faces
global global_faces_vel
global frame_missingbox
global frames
frames = 0
global_faces = ()
global_faces_vel = ()
frame_missingbox = 0

# only those faces having size > image size / 50 will be saved.
# e.g., given 800 x 600 input, the minimum face images saved will be about 98 x 98.
min_face_scale = 1/50.


import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', help='input dir', type=str, required=False)
parser.add_argument('-o', '--output', help='output dir', type=str, required=False)
parser.add_argument('-r', '--remove', help='remove old dir', type=bool, required=False)
parser.add_argument('-p', '--padding', help='padding', type=int, required=False)
args = parser.parse_args()


# ## 4. Crop faces
# Since dlib's cnn model performs really well on face deteciton, applying box-missing frame compensation is not needed.
# But for OpenCV's Haar-cascade Detection, compensating box-missing grame will increase the chance to crop face images in different angles.

# In[4]:

if args.padding:
	pad = args.padding
else:
	pad = 30
def process_image(input_img):   
    global global_faces
    global frame_missingbox
    global frames
    frames += 1

    # print (input_img)
    # Resize input image if necessary.
    img = input_img
    if img.shape[0]>800 or img.shape[1]>800:
        x ,y = img.shape[1]//5, img.shape[0]//5
        img = cv2.resize(input_img, (x*2,y*2))
    
    # print(img.shape,(x,y))
    # cv2.imshow("yfx",img)
    # cv2.waitKey(10000)
    # return 

    # img = img[:,:,::-1]
    # img = input_img
    faces = face_recognition.face_locations(img, model="cnn")
    size_img = img.shape[0] * img.shape[1]

    
    face_detected = False
    idx = 0
    # print(faces)
    for (x0,y1,x1,y0) in faces:
        print (np.abs((x1-x0) * (y1-y0)) , size_img * min_face_scale,pad)
        if np.abs((x1-x0) * (y1-y0)) > size_img * min_face_scale:
            #cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),5)
            #roi_gray = gray[y:y+h, x:x+w]
            try:
            	roi_color = img[x0-pad:x1+pad, y0-pad:y1+pad,:]
            	roi_color = cv2.resize(roi_color,(256,256))
            except:
            	roi_color = img[x0:x1, y0:y1,:]
            	roi_color = cv2.resize(roi_color,(256,256))

            fname = args.output+'/'+ str(frames) + "roi" + str(idx) + ".png"
            cv2.imwrite(fname, roi_color)
            # cv2.imshow(fname,roi_color)
            # cv2.waitKey(10000)
            idx += 1            
            global_faces = (x0,y1,x1,y0)
            frame_missingbox = 0
            face_detected = True
        else:
            face_detected = False
    
    # box-missing frame compensation
    #if not face_detected and frame_missingbox <= 5 and not global_faces is ():
    #    (x0,y1,x1,y0) = global_faces
    #    roi_color = img[x0:x1, y0:y1,:]
    #    frame_missingbox += 1       
    
    return img


# Function `process_image` will be called at each frame, and image of that frame will be the argument of `process_image`.


# In[13]:
import os
if not os.path.exists(args.output):
    os.mkdir(args.output)

# image = cv2.imread(args.input)
# process_image(image)

files = os.listdir(args.input)
for file in files:
    try:
        print (file)
        image = cv2.imread(args.input+'/'+file)
        process_image(image)
    except:
        pass

    # break
import gc
gc.collect()





# # Function `process_video` will be called at each frame, and image of that frame will be the argument of `process_video`.

# # In[13]:
# import os
# if not os.path.exists('./faces'):
#     os.mkdir('faces')

# output = '_.mp4'
# clip1 = VideoFileClip("INPUT_VIDEO.mp4")
# clip = clip1.fl_image(process_video)#.subclip(0,10) #NOTE: this function expects color images!!
# # get_ipython().run_line_magic('time', 'clip.write_videofile(output, audio=False)')
# clip.write_videofile(output, audio=False)

# # ## 5. Pack `./faces` folder into a zip file `./faces.zip`

# # In[9]:

# import gc
# gc.collect()

# import zipfile


# # In[10]:


# def zipdir(path, ziph):
#     # ziph is zipfile handle
#     for root, dirs, files in os.walk(path):
#         for file in files:
#             ziph.write(os.path.join(root, file))


# # In[15]:


# zipf = zipfile.ZipFile('faces.zip', 'w', zipfile.ZIP_DEFLATED)
# zipdir('faces/', zipf)
# zipf.close()

