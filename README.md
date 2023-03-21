# MMA Handicapping Model

> "Slow is smooth, smooth is fast" - Conor Mcgregor

Tracking mixed martial arts competitions and betting activity to identify optimal trading strategies. Take a statistical and automated approach to placing wagers on weekly events in an effort to maximize returns and minimize human engagement with detailed analysis. 

## Objective

Create a handicapping method that delivers supierior, and uncorrelated, returns to the market overtime (ex: SP 500, 10y Treasury, Nasdaq). 

## Inspiration

[Bill Benter](https://www.casino.org/blog/bill-benter/), a successful horse gambler active mostly in the 1990s in Hong Kong. 

## Programming Languages 

Python (scraping, cleaning), Python/R (regression analysis, cleaning). Beautifulsoup for web-scraping. Concurrency can help speed up scraping data.

## Data Sources

UFC Stats, BestFightOdds, Tapology.

Tapology contains the most granular data and also links BestFightOdds and UFC stats, which is extremely useful from a programming perspective. 

## Questions
Main focus questions:
* What are the main fighter characterics that influence win/lose probability?
* How random are fight outcomes?
* Can public odds markets accurately predict fight outcomes? 
* What types of fights are the most predictable/unpredictable?
* Is there enough publically available data to make informed decisions about fight outcomes?
* What is the best model choice for predicting fight outcomes?
* Can I create a specifc ELO system that seems to reflect other MMA ranking systems well? 

## Betting Sites

* FanDuel (NY)
* BetMGM  (NY)
* Caesars   (NY)
* WynnBET   (NY)
* BetRivers  (NY)  
* DraftKings (NY)
* PointsBet (NY)

## Attributes 

Variables:
* Fighter Age (at each event fight)
* Fighter height (constant)
* Fighter reach  (constant)
* Total fights   (before current fight)
* Previous fight result (need categorical variables)
* Days since last fight (or weeks, doens't matter that much)
* Has been KOed?  (over given history)
* Has been submitted? (over given history)
* Total fight time (this will be tricky)
* Total fight time in last fight (this should be manageable)

UFC Specific:
* Total strikes thrown
* Significant strike % accuracy
* Knowdown accuracy
* Takedown accuracy

