![Screenshot](https://github.com/wrcarpenter/MMA-Handicapping-Model/blob/main/Project-Image.jpg)

# Mixed Martial Arts (MMA) Betting Model

> "Slow is smooth, smooth is fast" - Conor Mcgregor

Tracking mixed martial arts competitions and betting activity to identify optimal trading strategies. Take a statistical and automated approach to placing wagers on weekly events in an effort to maximize returns and minimize human engagement with detailed analysis. 

## Objective

Create a betting strategy that outperforms generic approaches (random chance, bookmaker odds, etc) and delivers supierior, and uncorrelated, returns to the broader markests.

## Inspiration(s)

[Bill Benter](https://www.casino.org/blog/bill-benter/), a successful horse gambler active mostly during the 1990s in Hong Kong that one of the first to popularize quantitative betting models in a sports context.

Many notable figures are big fans of the UFC and broader MMA, such as Facebook founder [Mark Zuckerburg](https://en.wikipedia.org/wiki/Mark_Zuckerberg). He would surely be captivated by a data-driven perspective on the sport. 



## Data Sources 

|Name | Link | Description | 
| --- | --- | --- | 
| UFC Stats | [ufcstats.com](http://ufcstats.com/statistics/events/completed) | Historical UFC fight data and roster |
| Tapology  | [tapology.com](https://www.tapology.com/) | Comprehensive event and figter data across numerous MMA venues |
| Best Fight Odds | [bestfightodds.com](https://www.bestfightodds.com/) | Historical odds for MMA events from a variety of sportsbook platforms |

## Data Collection
UFC data currently scraped from UFC Stats site periodically.

## Preparing Data
Data cleaning process in progress.

## Model Design
Current model is simple logistical regression with variations on outcome (win, KO, submission, etc.).

Future model implementation should also account for public odds. 

## Some Focus Questions
A few main focus questions:
* What are the main fighter characterics that influence win/lose probability?
* How random are fight outcomes?
* Can public odds markets accurately predict fight outcomes? 
* What types of fights are the most predictable/unpredictable?
* Is there enough publically available data to make informed decisions about fight outcomes?
* What is the best model choice for predicting fight outcomes?
* Can I create a specifc ELO system that seems to reflect other MMA ranking systems well? 

## Betting Sites

* FanDuel (NY), BetMGM  (NY), Caesars   (NY), WynnBET   (NY), BetRivers  (NY), DraftKings (NY), PointsBet (NY)

