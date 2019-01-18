# Fusion360-WavyBowl
Fusion 360 script to create stacked wavy bowls

![Stacked wavy bowl](/images/bowl.png?raw=true)

## Overview
I own a [Glowforge](https://glowforge.us/BHZAKLOU) laser cutter and was intrigued by the idea of creating stacked bowls made from concentric wavy rings that are rotated and glued to make a bowl.  After a few attempts to model them in Fusion 360 to understand the curves, I realized I wanted to do enough experimentation to get the look right that it was worth some scripting to iterate quickly - a few days later, this is the result.

## Usage
* Run Fusion 360.
* First usage: In a new document, press `shift + S` to open the scripts dialog, hit the green + sign next to "My Scripts" and select the folder you've downloaded the manifest and py files to.
* Run the script and play with the settings
* Do whatever you normally do to create a laser path from a Fusion object
  * I use [Colorific](https://github.com/garethky/glowforge-colorific-fusion360-post) to get a good output for my [Glowforge](https://glowforge.us/BHZAKLOU)

## Options
![Options dialog](/images/options.png?raw=true)

Most options should be obvious but a few notes:
* Amplitude % is the percentage of the ring width for the wave - basically, how wavy is it.  I found that it was needed to vary this across the bowl to get a pleasing shape, which is why there are two sliders.  The first is what the first ring will use, the second is for the last ring.
* Curve: default is 0 which means all the rings are the same size.  The slider allows you to pick a percentage of size the first ring is from the average and then vary the size through the rings (the middle ring will be the same with all settings).  This gives the bowl more of a curve from the side view instead of the default straight slope.  Definitely changes the look a bunch, sometimes not for the better.
* Flatten: this allows for not stacking the resulting rings - depending on your method of exporting paths for laser cutting, this might be easier to use.
* Overall bowl diameter is appended to the Component name so that you know how much material will be needed.
* Be careful with the number of rings + waves you choose, processing time can get long...

## License
No restrictions on using this to make objects to give away or sell - I don't need acknowledgement and you don't need my permission.  I'd love to hear about anything you do create with this script or if you have thoughts or suggestions for improvements! 