# Overview of core functionalities

# Trustworthiness calculation

The trustworthiness score is an integer value in the range [0..5]. It is being calculated based on a variety of factors 
described below.

## Stored in database?
The score is stored in the database to enable the tracking of its history. This offers the user the option to evaluate
how the trustworthiness of an NGO has developed over time.

Stored in the database:
- total trustworthiness score
- score resulting from the credibility of its data source
- score resulting from the number of data sources it is being derived from
- score resulting from its accreditations

Storing these individual factors enables offering a detailed history of the trustworthiness score.

:exclamation: This means that the score has to be updated every time an influencing factors is added or updated.

## Which factors are currently being used?

- credibility of data source(s)
- number of data sources
- [ECOSOC](https://csonet.org/?menu=100) accreditation 


## What additional features could potentially be used in the future?
- use more of the accreditations listed in the database
- query [UN ECOSOC](https://esango.un.org/civilsociety/displayConsultativeStatusSearch.do?method=search&sessionCheck=false)
for more accreditation information (also lists other accreditations)
- user ratings
- reported scandals
- NGO size (members, staff; could disadvantage smaller NGOs)
- age of NGO

## What are the requirements to currently receive an optimal trustworthiness score? 

- listed by one credible source
- listed by all data sources
- ECOSOC accredited


## What is the current score distribution?
| Score | # NGOs |
| ----- | ------: |
| 0 | 687 |
| 1 | 0 |
| 2 | 0 |
| 3 | 269 |
| 4 | 44 |
| 5 | 1 |


## How is the score calculated?

Most straightforward option:
- max. number of data sources: 2
- max. credibility: (# data sources) x yes
- max. accreditation: ECOSOC yes

However, an NGO should not be punished with a lower rating simply because we add a new, less credible data-source.
It should be possible to obtain the optimal score with only one credible data source.

Further considerations:
- an NGO with one credible data source should have a better rating than an NGO with multiple less credible sources
- but the number of data sources should be correlated to the score
- more than one credible source does not make the NGO more credible


The following factors will be used:

| Factor                | Value                        | current max. value |Reasoning |
| --------------------- | ----------------------------- | -------- | --------- |
| # data sources        | 1 per source | 2 | |
| one credible source   | (# data sources overall) * 2 + 1  | 5 | one credible source > all (less) credible sources combined + ECOSOC |
| ECOSOC                | # data sources overall | 2 | ECOSOC does not hold as much meaning without a credible source |


score_raw(NGO) = (# data sources listing NGO) + (credible_source(NGO)) + ECOSOC(NGO)

Since the score has to be scaled into the range [0..5], use the following [formula](https://stats.stackexchange.com/questions/281162/scale-a-number-between-a-range/281164) to achieve this:

| Variable | Value | Description |
| -------- | ----- | ----------- |
| r<sub>min</sub> | 1 | min. value of raw TW score (i.e. one data source and nothing else) |
| r <sub>max</sub> | 9 | max. value of raw TW score |
| t<sub>min</sub> | 0 | min. value of TW score |
| t<sub>max</sub> | 5 | max. value of TW score |

TW_score = [(TW_score_raw - r<sub>min</sub>) / (r<sub>max</sub> - r<sub>min</sub>)] * (t<sub>max</sub> - t<sub>min</sub>) + t<sub>min</sub>


## When will the score be calculated?
During the initial data import, the score will be calculated. There also exists a URL to recalculate the score for all
 NGOs in the database if necessary (e.g. if the score calculation was modified). There is currently no feature that would 
 automatically recalculate the score, for example when an object is saved to the database. Instead, use the `TWCalculator`
 to calculate the new trustworthiness score after changes to the NGO's data were made.
 It is possible to include a recalculation of the tw score into the `save`-method of database objects. This should be 
 discussed further.