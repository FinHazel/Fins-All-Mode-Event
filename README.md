# Taiko Team Festival - Fin's All Mode Event

Program used to balance teams in Taiko Team Festival, which has been repurposed for Fin's All Mode Event.

The algorithm used here forms teams and tries to swap players around to minimize a metric which represents how unbalanced a team is.
The metric we have chosen has two parts :

* How close the sum of all map seedings of all players are to the expected value (how good a team is overall)
* How close the sum of map seedings of all players are to the expected value on each map (how well-rounded the team is)

Please read the code for more information on how it is actually implemented.

This code was written for the most part by 49Leo. Thanks to Briesmas for helping with some parts of the code and Chupalika for providing the json file.



For TTF2, the following changes have been implemented :

* Players are no longer divided into A/B/C/D seeds.
* Timezones are no longer taken into consideration.

FAME uses the exact same version as TTF2.