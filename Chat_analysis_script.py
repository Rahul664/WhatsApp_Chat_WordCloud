# Created by RAHUL S H on 4/26/20
#rhoskeri50@gmail.com

import csv
import re
import os
import numpy as np
import pandas as pd
from PIL import Image
from wordcloud import WordCloud , STOPWORDS , ImageColorGenerator
import matplotlib.pyplot as plt

# Reading the imput chat text file
reading_input_file = open ( os.getcwd()+"/"+input("Enter the full file name with .txt extensions  ") , "r" )

# Data Declaration Section
lines = reading_input_file.readlines ( )  # Read lines from the file
# word_dictionary={} # Dictionary to hold the words and their count

# Data Processing
total_number_of_lines = len ( lines )  # Total number of lines in the text file

# Extract date
# date=re.match(r'[\d]{1,2}/[\d]{1,2}/[\d]{1,2}',lines[1158].split()[0].rstrip(","))[0]
# print(date)

# #Extract time
# print(lines[2].split()[1]+lines[2].split()[2])

# #Extract Name
# print(lines[2].split("-")[1].split(":")[0])

# #Extract Message
# print(lines[2].split("-")[1].split(":")[1])

# Writing to csv file
output_file_name = \
    reading_input_file.name.split ( "/" ) [ len ( reading_input_file.name.split ( "/" ) ) - 1 ].split ( "." ) [
        0 ] + ".csv"
output_csv = open ( output_file_name , 'w+' )
csv_write = csv.writer ( output_csv )
csv_write.writerow ( [ "Date" , "Time" , "Name" , "Message" ] )
for i in range ( 1 , total_number_of_lines ) :
    try :
        date = re.match ( r'[\d]{1,2}/[\d]{1,2}/[\d]{1,2}' , lines [ i ].split ( ) [ 0 ].rstrip ( "," ) ) [ 0 ]
        time = lines [ i ].split ( ) [ 1 ] + lines [ i ].split ( ) [ 2 ]
        name = lines [ i ].split ( "-" ) [ 1 ].split ( ":" ) [ 0 ]
        message = lines [ i ].split ( "-" ) [ 1 ].split ( ":" ) [ 1 ]
        csv_write.writerow ( [ date , time , name , message ] )
    except :
        message = lines [ i ]
        csv_write.writerow ( [ date , time , name , message ] )

# Reading output csv file
output_lines = pd.read_csv ( os.getcwd ( ) + "/" + output_file_name )  # Read csv file with pandas into data frame

# Plot by statistics gouped by Name
# stat_name= output_lines.groupby("Name").describe()
# stat_name.plot.bar()
# plt.title("Group by Name Bar Chart")
# plt.show()
# # Plot by grouped by date
# name_date_df=output_lines[["Date","Name","Time"]]
# stat_date=name_date_df.groupby("Date").describe()
# stat_date.plot.bar()
# print(stat_date)
# plt.title("Group by Date Bar Chart")
# plt.show()
# # print(groupby_name.head())

#Create WordCloud
text_df=output_lines[["Message"]]
text=" ".join(msg for msg in text_df.Message)

#setting stopwords that you want to ignore
stopwords=set(STOPWORDS)
stopwords.update(["Media","omitted"])

#convert image to greyscale with PIL library
grey_image_input=input("Enter the image name with .png extension ")
grey_image=Image.open(os.getcwd()+"/"+grey_image_input)
grey_image.convert(mode='L').save("grey_output.png")
#load greyscale as np array and perform masking

image=np.array(Image.open("grey_output.png"))
mask=image<1
image[mask]=255
plt.imshow(image,'gray')
#generate wordcloud
wordcloud=WordCloud(background_color="white",mask=image,contour_width=3,contour_color="black",stopwords=stopwords)
wordcloud.generate(text)
plt.imshow(wordcloud)
plt.axis("off")
plt.savefig(os.getcwd()+"/"+"word_cloud_output")
plt.show()