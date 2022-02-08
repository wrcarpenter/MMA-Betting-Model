# MMA-Bout-Model

Tracking mixed martial arts competitions and betting activity to identify optimal trading strategies. Take a statistical and automated approach to placing wagers on weekly events in an effort to maximize returns and minimize human engagement with detailed analysis. 

## Programming Languages 

Python (scraping, cleaning), Stata (regression analysis, cleaning). Use Beautifulsoup or Selenium for web-scraping. Concurrency can help speed up scraping data.

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

## Attributes 

Variables:
* Fighter Age
* Fighter height 
* Fighter reach 
* Total fights 
* Previous fight result
* Days since last fight 
* Has been KOed?
* Has been submitted?
* Total fight time
* Total fight time in last fight

