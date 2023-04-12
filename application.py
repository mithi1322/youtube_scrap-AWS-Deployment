from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
from urllib.request import urlopen as uReq
import pymongo
import os
import shutil
import re
import csv

application = Flask(__name__) # initializing a flask app
app=application

@app.route('/',methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")

@app.route('/review',methods=['POST','GET']) # route to show the videos link,thumbnails,views,publish_time in a web UI
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            searchString = request.form['content'].replace(" ","")
            # fake user agent to avoid getting blocked by Google
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}
            # fetch the search results page
            youtube_url = (f"https://www.youtube.com/@{searchString}/videos")
            youtube_channal =requests.get(youtube_url)
            res=youtube_channal.text
            
               # videos url
            videoids = re.findall('"videoRenderer":{"videoId":".*?"', res)
                # thumbnail
            thumbnails = re.findall('"thumbnail":{"thumbnails":\[{"url":".*?"', res)
                # title
            titles = re.findall('"title":{"runs":\[{"text":".*?"', res)
                # views
            views = re.findall('"shortViewCountText":{"accessibility":{"accessibilityData":{"label":".*?"', res)
                # published Time
            published_time = re.findall('"publishedTimeText":{"simpleText":".*?"', res)

            filename = searchString+ ".csv"
            fw = open(filename, "w")
            headers = "Sr.No.,Videoids, Thumbnails, Titles, Views, Published Time \n"
            fw.write(headers)
            reviews = []
            #report_list =['S No', 'Video url', 'Thumbnails', 'Titles', 'Views', 'Published Time']
            for i in range(6):
                video_url="https://www.youtube.com/watch?v="+videoids[i].split('"')[-2]
                thumbnail=thumbnails[i].split('"')[-2]
                title=titles[i].split('"')[-2]
                view=views[i].split('"')[-2]
                published_times=published_time[i].split('"')[-2]
            
                mydict = {"Sr.No.":i+1, "Videos Url": video_url, "Thumbnails": thumbnail, "Titles": title,"Views": view,"Published_Time":published_times}
                reviews.append(mydict)

            return render_template('results.html', reviews=reviews[0:(len(reviews)-1)])
            # return "Success"
        except Exception as e:
            print("The Exception message is: ",e)
            return "Please check that you have typed the correct Username"
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
	#app.run(debug=True)
