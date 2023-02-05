## Key Variables

Key variables:
* Height
* Reach
* Weight class
* Age at time of fight
* Time since last fight
* Average time between fights (for this fighter) vs overall average time for all fighters? 
* Total Fights
* Total Fight Time
* Overall record 
* Result of last fight
* Result of second to last fight
* Ever been KOed?
* Ever been submitted?

## Current Process

Build robust dataset (updated periodically) and model for UFC Stats data. Use this model for betting strategies. Try to add odds data to prediction strength.

If interesting/successful, add Tapology data. Otherwise, finalize project. 

## Current Errata

Initialize variables to avoid repeats with blank data. 

Record strikes/takedowns/etc. just to have that data in case of future applicability. 

Important Missing Data:
* Birthday
* Reach
* Height
* Stance (switch, southpaw, orthodox, other, none)
* Style? (BJJ, wrestling, striker, etc.) 

## Data Update Process

Update all past and upcoming events. Get information on number of completed fights. 

(Create a comprehensive scraper to do a one-time large collection of fighter data for data set birth).

Run routine update for new fighter data that can be added to current data set. Save this data set as a raw/current version.

Generate all relevant variables for the datset and save that data set. 

Run routine questions through the data set on betting simulations and create a betting model.



