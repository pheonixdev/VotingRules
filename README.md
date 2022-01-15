# VotingRules
Python program to implement several voting rules. In a voting setting, we have a set of n agents and a set of m alternatives. Every agent has a preference ordering > where 
a > b means that the agent prefers alternative a to alternative b. A preference profile is a set of n preference orderings, one for every agent.

For example, if we have a voting setting with 4 agents and 4 alternatives, one possible preference profile could be the following:

Agent 1: a > b > d > c
Agent 2: b > a > c > d
Agent 3: b > c > a > d
Agent 4: d > c > a > b

A voting rule is a function that takes as input the preferences of a set of agents and outputs a winning alternative.

Consider the following voting rules:

* [Dictatorship](#dictatorship) : An agent is selected, and the winner is the alternative that this agent ranks first. For example, if the preference ordering of the selected agent is a > c > b > d, then the winner is alternative a.

* [scoringRule](#scoringRule) : The function should input a preference profile represented by a dictionary. A score vector of length m, i.e., equal to the number of alternatives, i.e., a list of length  containing positive floating numbers.
For every agent, the function assigns the highest score in the scoring vector to the most preferred alternative of the agent, the second highest score to the second most preferred alternative of the agent and so on, and the lowest score to the least preferred alternative of the agent. In the end, it returns the alternative with the highest total score, using the tie-breaking option to distinguish between alternatives with the same score.

* [Plurality](#Plurality) : The winner is the alternative that appears the most times in the first position of the agents' preference orderings. In the case of a tie, use a tie-breaking rule to select a single winner.

* [Veto](#Veto) : Every agent assigns 0 points to the alternative that they rank in the last place of their preference orderings, and 1 point to every other alternative. The winner is the alternative with the most number of points. In the case of a tie, use a tie-breaking rule to select a single winner.

* [Borda](#Borda) : Every agent assigns a score of 0 to the their least-preferred alternative (the one at the bottom of the preference ranking), a score of 1 to the second least-preferred alternative, ... , and a score of m-1 to their favourite alternative. In other words, the alternative ranked at position j receives a score of m-j. The winner is the alternative with the highest score. In the case of a tie, use a tie-breaking rule to select a single winner.

* [Harmonic](#Harmonic) : Every agent assigns a score of  to the their least-preferred alternative (the one at the bottom of the preference ranking), a score of  to the second least-preferred alternative, ... , and a score of  to their favourite alternative. In other words, the alternative ranked at position  receives a score of . The winner is the alternative with the highest score. In the case of a tie, use a tie-breaking rule to select a single winner.

* [Single Transferable Vote](#SingleTransferableVote)(STV) : The voting rule works in rounds. In each round, the alternatives that appear the least frequently in the first position of agents' rankings are removed, and the process is repeated. When the final set of alternatives is removed (one or possibly more), then this last set is the set of possible winners. If there are more than one, a tie-breaking rule is used to select a single winner.

* [rangeVoting ](#rangeVoting ) :The function should input a worksheet corresponding to an xlsx file. The function should return the alternative that has the maximum sum of valuations, i.e., the maximum sum of numerical values in the xlsx file, using the tie-breaking option to distinguish between possible winners.

### Tie-Breaking Rules:
We will consider the following three tie-breaking rules. Here, we assume that the alternatives are represented by integers.
* [max](#max): Among the possible winning alternatives, select the one with the highest number.
* [min](#min): Among the possible winning alternatives, select the one with the lowest number.
* [agent i](#agent) : Among the possible winning alternatives, select the one that agent  ranks the highest in his/her preference ordering. 
