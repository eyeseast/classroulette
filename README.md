Class Roulette
==============

Get a random lecture.

How it works
------------

There are thousands of lectures on YouTube. [Here's Yale](http://www.youtube.com/user/YaleCourses). Let's pull those in and serve a random one everytime you load. Use it as background noise or to go to sleep at night.

Pull in an RSS feed of videos. Store the user:video_id pairs for each video URL in a Redis set. Pull in video details from the YouTube (v2) API on display (so it's always up to date).


TODO:
-----

 - buy a domain
 - analytics
 - ads
 - channels?