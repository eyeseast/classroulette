Class Roulette
==============

Get a random lecture.

How it works
------------

There are thousands of lectures on YouTube. [Here's Yale](http://www.youtube.com/user/YaleCourses). Let's pull those in and serve a random one everytime you load. Use it as background noise or to go to sleep at night.

Pull in an RSS feed of videos. Store the user:video_id pairs for each video URL in a Redis set. Pull in video details from the YouTube (v2) API on display (so it's always up to date).

Videos should be shown randomly. To test this, each video returned is logged in a Redis sorted set. This should produce a reasonably even distribution.

TODO:
-----

 - video stats
 - FB meta
 - Twitter card
 - share buttons
 - channels?