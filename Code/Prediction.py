from tkinter.constants import S

def pred_main():
    # importing necessary libraries
    import cv2
    import imutils
    import numpy as np
    import os
    import pickle
    import pyttsx3
    import tensorflow as tf
    from tensorflow import keras
    import keras
    from threading import Thread
    from tkinter import messagebox
    import tkinter as tk
    import SpellChecker


    #global variables
    bg=None
    visual_dict={0:'0',1:'1',2:'2',3:'3',4:'4',5:'5',6:'6',7:'7',8:'8',9:'9',10:'a',11:'b',12:'c',13:'d',14:'e',15:'f',16:'g',17:'h',18:'i',19:'j',20:'k',21:'l',22:'m',23:'n',24:'o',25:'p',26:'q',27:'r',
             28:'s',29:'t',30:'u',31:'v',32:'w',33:'x',34:'y',35:'z'}
    aWeight=0.5
    cam=cv2.VideoCapture(cv2.CAP_DSHO)
    #t,r,b,l=100,350,228,478

    # Global Variables
    t,r,b,l=100,350,325,575
    num_frames=0
    cur_mode=None
    predict_sign=None
    count=0
    shape=180
    result_list=[]
    words_list=[]
    text=''
    correct_word=''
    final_sign=''
    sentence=''
    prev_sign=None
    count_same_sign=0

    method = 1

    model='CNN'

    infile = open(model,'rb')
    cnn = pickle.load(infile)
    infile.close()

    bg=None
    count=0

    #To find the running average over the background
    def run_avg(image,aweight):
        nonlocal bg #initialize the background
        if bg is None:
            bg=image.copy().astype("float")
            return
        cv2.accumulateWeighted(image,bg,aweight)

    #Segment the egion of hand
    def extract_hand(image,threshold=25):
        nonlocal bg
        diff=cv2.absdiff(bg.astype("uint8"),image) 

        thresh=cv2.threshold(diff,threshold,255,cv2.THRESH_BINARY)[1]
        (_,cnts,_)=cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        
        if(len(cnts)==0):
            return
        else:
            max_cont=max(cnts,key=cv2.contourArea)
            return (thresh,max_cont)

    engine=pyttsx3.init()
    engine.setProperty("rate",100)
    voices=engine.getProperty("voices")
    engine.setProperty("voice",voices[1].id)
    
    spell = SpellChecker()    

    def say_text(sign):
        print(sign)
        while engine._inLoop:
            pass
        engine.say(sign)
        engine.runAndWait()

    def say_word(word):
        nonlocal correct_word, sentence
        mispelled_word = spell.unknown([word])
        
        print(correct_word)
        # if word is misspelled, correct
        if (len(mispelled_word)):
            correct_word = spell.correction(mispelled_word.pop())
        else:
            correct_word = word
        
        if (sentence):
            sentence += ' ' + correct_word
        else:
            sentence += correct_word

        while engine._inLoop:
            pass
        engine.say(correct_word)
        engine.runAndWait()

    def n(x):
        pass

    if method == 2:
        cv2.namedWindow('Tracking', cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Tracking", 640, 480)
        cv2.createTrackbar("LH", "Tracking", 0, 255, n)
        cv2.createTrackbar("LS", "Tracking", 0, 255, n)
        cv2.createTrackbar("LV", "Tracking", 0, 255, n)
        cv2.createTrackbar("UH", "Tracking", 255, 255, n)
        cv2.createTrackbar("US", "Tracking", 32, 255, n)
        cv2.createTrackbar("UV", "Tracking", 255, 255, n)

    while(cam.isOpened()):
        _,frame=cam.read(cv2.CAP_DSHOW)
        if frame is not None:
            frame=imutils.resize(frame,width=700)
            frame=cv2.flip(frame,1)
            clone=frame.copy()

            # height,width=frame.shape[:2]
            roi=frame[t:b,r:l]

            if method==1:
                gray=cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)   # rgb to grayscale
                #cv2.imshow("GrayScale",gray)
                gray=cv2.GaussianBlur(gray,(7,7),0)        
                #cv2.imshow("Gaussian Blur",gray)

                # first 30 frames are considered as background and any new object in the frame is then filtered out
                if(num_frames<30):
                    run_avg(gray,aWeight)
                    cv2.putText(clone, "Keep the Camera still.", (10, 100), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 0))
                else:
                    hand=extract_hand(gray)
                    if hand is not None:
                        thresh,max_cont=hand
                        
                        mask=cv2.drawContours(clone,[max_cont+(r,t)],-1, (0, 0, 255))
                        #cv2.imshow("Threshold",thresh)
                        mask=np.zeros(thresh.shape,dtype="uint8")

                        cv2.drawContours(mask,[max_cont],-1,255,-1)

                        mask = cv2.medianBlur(mask, 5)
                        
                        mask = cv2.addWeighted(mask, 0.5, mask, 0.5, 0.0)

                        kernel = np.ones((5, 5), np.uint8)

                        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)


                        res=cv2.bitwise_and(roi,roi,mask=mask)
                        res=cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)

                        high_thresh, thresh_im = cv2.threshold(res, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                        
                        lowThresh = 0.5 * high_thresh

                        #cv2.imshow("Segmented",res)
                        hand=cv2.bitwise_and(gray,gray,mask=thresh)
                        cv2.imshow("Hand",hand)
                        res = cv2.Canny(hand, lowThresh, high_thresh)
                        #cv2.imshow("Canny Edge",res)


                        # CNN Model
                        if res is not None and cv2.contourArea(max_cont) > 1000:
                            final_res = cv2.resize(res, (100, 100))
                            final_res = np.array(final_res)
                            final_res = final_res.reshape((-1, 100, 100, 1))
                            final_res.astype('float32')
                            final_res = final_res / 255.0
                            output = cnn.predict(final_res)
                            prob = np.amax(output)
                            sign = np.argmax(output)
                            final_sign = visual_dict[sign]

                            count += 1
                            if (count > 10 and count <= 70):
                                if (prob * 100 > 97):
                                    result_list.append(final_sign)

                            elif (count > 70):
                                count = 0
                                if len(result_list):
                                    predict_sign = (max(set(result_list), key=result_list.count))
                                    result_list = []
                                    if (not words_list):
                                        text = ""
                                        correct_word = ""
                                    if prev_sign != predict_sign:
                                        print(words_list)
                                        words_list += str(predict_sign)
                                        text += str(predict_sign)
                                        Thread(target=say_text, args=(predict_sign,)).start()
                                        # prev_sign=predict_sign
                                    prev_sign = predict_sign
                                # print(words_list)
                                # cv2.putText(clone,'Sign'+str(predict_sign), (100, 300), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 0))

                        else:
                            if words_list is not None and words_list:
                                print(words_list)
                                Thread(target=say_word,args=(text,)).start()
                                words_list.clear()

            cv2.rectangle(clone, (l, t), (r, b), (0, 255, 0), 2)
            num_frames += 1

            blackboard = np.zeros((480, 640, 3), dtype=np.uint8)
            cv2.putText(blackboard, "ISL Recognition", (180, 50), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0, 0,255))
            cv2.putText(blackboard, 'Sign: ' + str(final_sign), (30, 100), cv2.FONT_HERSHEY_TRIPLEX, 1, (120, 252,0))
            cv2.putText(blackboard, "Recognising Word - " + text, (30, 130), cv2.FONT_HERSHEY_TRIPLEX, 1, (120, 252,0))
            cv2.putText(blackboard, "Correct Word - " + correct_word, (30, 160), cv2.FONT_HERSHEY_TRIPLEX, 1, (120, 252,0))
            cv2.putText(blackboard, "Sentence - " + sentence, (30, 190), cv2.FONT_HERSHEY_TRIPLEX, 1, (120, 252,0))


            cv2.putText(blackboard, "Press enter for new sentence.", (30, 300), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255))
            cv2.putText(blackboard, "Press esc to exit.", (30, 320), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255))
            cv2.putText(blackboard, "Keep the Camera still.", (30, 340), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255))
            cv2.putText(blackboard, "Put your hand in the rectangle", (30, 360), cv2.FONT_HERSHEY_COMPLEX, 0.5,(255, 255, 255))

            orig_signs=cv2.imread('files/signs.png')
            signs=cv2.resize(orig_signs,(640, 480))
            cv2.imshow("Signs", signs)
            clone=cv2.resize(clone,(640, 480))

            blackboard = np.hstack((clone, blackboard))
            cv2.imshow("Indian Sign Language Recognition", blackboard)

        else:
            messagebox.showerror("error","Can't grab frame")
            break

        k=cv2.waitKey(1)& 0xFF
        # new sentence if enter is pressed
        if (k==13):
            Thread(target=say_text,args=(sentence,)).start()
            sentence = ''

        # close if esc is pressed
        if (k==27):
            break



    cam.release()
    cv2.destroyAllWindows()