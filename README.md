# Data Challenge
A business question we ran into

We sometimes run a/b tests. the main difficulty we face in doing this is, we sometimes do not know what to do and how to interpret results.

For instance: If we have 100 participants in our test group and 98 of those are converting towards a certain goal, while we also have 100 participants in our control group and of those we see only 10 users converting, it is very clear: we should go for the test.

But in real life it unfortunately is not always that obvious... We sometimes do not really know if a result is meaningful or not. This is, what this test is about.

We conducted an a/b-test about recommendation sliders we implemented. Now we want to know what the test results tell us.

We will go through everything in detail in the next steps.
Import everything that is necessary in this section

You don't have to do it now. You can also do it later. But please put everything you import here.


## Reading csv

Please start here:
The name of the csv file is 'ga_data_rndm.csv'
It shows randomized sample data from our google analytics account.

## Explanations on the dataframe

dimension13 indicates the testgroups the users were in.

Recommendation Slide:0  always means control group

Recommendation Slide:1  always means test group

If there is no 'Recommendation Slide' in dimension13 it means, the users did not participate in the test. If there are also other strings in dimension13 (like "Second Technical 50:0" or something) those values indicate other tests that ran at the same time. But we are not interested in the results of those tests?


In short: In other groups, beside 'Recommendation Slide', we are not interested.

## Please help us making sense out of this data

After exploring the data: What can you tell us by looking at the data? What conclusions do you have?

What does this mean for us and our test?

Especially with regards to our test: What should we do and how should we proceed?

Is there anything specific with regards to device categories?

Any other things you noticed or found interesting?

Please back your findings with visualisations and aggregated tables

Good luck! We are very excited to discuss the findings you have with you.
