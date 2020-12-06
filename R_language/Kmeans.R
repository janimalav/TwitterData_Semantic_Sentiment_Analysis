install.packages(stats)
#load
library(stats)
library(dplyr)
library(ggplot2)
library(ggfortify)
#get data
tuna <- read.csv('timestamp.csv',TRUE)
tuna.mydata <- tuna
head(tuna.mydata)
km <- kmeans(centers = 8,tuna.mydata)
head(km)
km$centers
head(tuna.mydata)
v1 = tuna.mydata$dateTime
v2 = tuna.mydata$time

ggplot() +
  geom_point(data = tuna.mydata, 
             mapping = aes(x = dateTime, 
                           y = time, 
                           colour = km$cluster)) +
  geom_point(mapping = aes_string(x = km$centers[, "dateTime"], 
                                  y = km$centers[, "time"]),
             color = "red", size = 4)
