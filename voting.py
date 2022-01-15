
"""This is a program that implements several voting rules based on the preferences of alternatives from different agents.
The following voting rules are implemented in the program: Dictatorship, Plurality, Veto, Borda, Harmonic, Single Transferable Vote (STV).
In addition to these, two other functions, scoringRule and rangeVoting are also implemented. 
A tie break option is also included in the case of multiple winners with the same preference.
"""
import copy


def generatePreferences(values):
    """Function to input values that the agents have for the different alternatives and outputs a preference profile.
    The input values to the generatePreferences function is a worksheet corresponding to an xlsx file.
    The rows of the file correspond to agents and the columns correspond to alternatives.
    The value of a cell  is a numerical value that signifies how happy the agent would be if that alternative were to be selected.

    Args:
        values (file): worksheet corresponding to an xlsx file
        
    Returns:
        dict : dictionary where the keys are the agents and the values are lists that correspond to the preference orderings of those agents
    """
    agent_dict = {}
    temp_dict = {}
    for row in range(1, values.max_row + 1):
        key = row
        if key not in agent_dict.keys():
            agent_dict[key] = []
        for col in range(1, values.max_column + 1):
            agent_dict[key].append(values.cell(row, col).value)

    # the values are sorted to store the preferences of the agents
    for key, values in agent_dict.items():
        temp_dict = {index + 1 : val for index, val in enumerate(values)}
        agent_dict[key] = sorted(temp_dict, key=temp_dict.get)[::-1]
    return agent_dict


def dictatorship(preferenceProfile, agent):
    """Function to determine the winner where an agent is selected, and the winner is the alternative that this agent ranks first.

    Args:
        preferenceProfile (dict): dictionary with the preferences of agents
        agent (int): The value of the agent to determine the preference
        
    Returns:
        int : final winner of the voting rule
    """
    try:
        if agent in preferenceProfile.keys():
            winner = preferenceProfile[agent][0]
            return winner
        else:
            raise ValueError      
    except ValueError:
        print("Not an agent")


def scoringRule(preferences, scoreVector, tieBreak): 
    """For every agent, the function assigns the highest score in the scoring vector to the most preferred alternative of the agent,
    the second highest score to the second most preferred alternative of the agent and so on,
    and the lowest score to the least preferred alternative of the agent.
    In the end, it returns the alternative with the highest total score, using the tie-breaking option to distinguish between alternatives with the same score.

    Args:
        preferences (dict): dictionary with the preferences of agents
        scoreVector (list): positive floating numbers with length of total alternatives
        tieBreak (int, 'min', 'max'): determines the winner incase of a tie break 
        
    Returns:
        int : final winner of the voting rule
    """
    score_dict = {}
    winner = list()
    alternate_len = len(preferences[1])
    try:
        if len(scoreVector) != alternate_len:
            raise ValueError
        for key in preferences.keys():
            temp_dict = dict(zip(preferences[key], sorted(scoreVector, reverse=True)))
            for key, values in temp_dict.items(): 
                score_dict[key] = score_dict.get(key, 0) + values
    except ValueError:
        print("Incorrect input")

    winner = get_max_val(score_dict)
    return tie_break(preferences, tieBreak, winner)


def plurality(preferences, tieBreak):
    """Function to return the winner which is the alternative that appears the most times in the first position of the agents' preference orderings

    Args:
        preferences (dict): dictionary with the preferences of agents
        tieBreak (int, 'min', 'max'): determines the winner incase of a tie break 
        
    Returns:
        int : final winner of the voting rule
    """
    temp_dict = {}
    votes = {}
    winner = list()
    for key, values in preferences.items():
        temp_dict[key] = values[0]
    for values in temp_dict.values():
        if values in votes.keys():
            votes[values] += 1
        else:
            votes[values] = 1

    winner = get_max_val(votes)
    return tie_break(preferences, tieBreak, winner)


def veto(preferences, tieBreak):
    """Function to return the winner where every agent assigns 0 points to the alternative that they rank in the last place of their preference orderings,
    and 1 point to every other alternative. The winner is the alternative with the most number of points

    Args:
        preferences (dict): dictionary with the preferences of agents
        tieBreak (int, 'min', 'max'): determines the winner incase of a tie break 
        
    Returns:
        int : final winner of the voting rule
    """
    temp_dict = {}
    winner = list()
    for key, values in preferences.items():
        for element in values:
            if element not in temp_dict:
                temp_dict[key] = 0
    for values in preferences.values():
        for item in values[:-1]:
            temp_dict[item] += 1

    winner = get_max_val(temp_dict)
    return tie_break(preferences, tieBreak, winner)


def borda(preferences, tieBreak):
    """Function to return the winner where every agent assigns a score of 0 to the their least-preferred alternative (the one at the bottom of the preference ranking),
    a score of 1 to the second least-preferred alternative, ... , and a score of m-1 to their favourite alternative.
    In other words, the alternative ranked at position j receives a score of m-j. The winner is the alternative with the highest score

    Args:
        preferences (dict): dictionary with the preferences of agents
        tieBreak (int, 'min', 'max'): determines the winner incase of a tie break 
        
    Returns:
        int : final winner of the voting rule
    """
    temp_dict = {}
    winner = list()
    alternate_len = len(preferences[1])
    for key, values in preferences.items():
        for element in values:
            if element not in temp_dict:
                temp_dict[key] = 0
    for values in preferences.values():
        for item in values[:-1]:
            temp_dict[item] += alternate_len - (values.index(item) + 1)

    winner = get_max_val(temp_dict)
    return tie_break(preferences, tieBreak, winner)


def harmonic(preferences, tieBreak):
    """Function to return the winner where every agent assigns a score of 1/m to the their least-preferred alternative (the one at the bottom of the preference ranking),
    a score of 1/(m-1) to the second least-preferred alternative, ... , and a score of 1 to their favourite alternative.
    In other words, the alternative ranked at position j receives a score of 1/j. The winner is the alternative with the highest score

    Args:
        preferences (dict): dictionary with the preferences of agents
        tieBreak (int, 'min', 'max'): determines the winner incase of a tie break 
        
    Returns:
        int : final winner of the voting rule
    """
    temp_dict = {}
    winner = list()
    alternate_len = len(preferences[1])
    for key, values in preferences.items():
        for element in values:
            if element not in temp_dict:
                temp_dict[key] = 0
    for values in preferences.values():
        for item in values:
            temp_dict[item] += 1/(alternate_len - (alternate_len - (values.index(item) + 1)))

    winner = get_max_val(temp_dict)
    return tie_break(preferences, tieBreak, winner)


def STV(preferences, tieBreak):
    """Function to return the winner in rounds where in each round, 
    the alternatives that appear the least frequently in the first position of agents' rankings are removed, and the process is repeated.
    When the final set of alternatives is removed (one or possibly more), then this last set is the set of possible winners

    Args:
        preferences (dict): dictionary with the preferences of agents
        tieBreak (int, 'min', 'max'): determines the winner incase of a tie break 
        
    Returns:
        int : final winner of the voting rule
    """
    # copy used so that original preferences will be unaltered
    temp_dict = copy.deepcopy(preferences)
    while True:
        frequency = dict.fromkeys(temp_dict[1], 0)
        for values in  temp_dict.values():
            frequency[values[0]] += 1

        # the lowest value is calculated and appended to least list
        least = list()
        min_value = min(frequency.values())
        for key, values in frequency.items():
            if values == min_value:
                least.append(key)
        
        if len(least) == len(temp_dict[1]):
            return tie_break(preferences, tieBreak, least)

        # least frequest alternative removed from dictionary
        else:
            for item in least:
                frequency.pop(item, None)
            for values in temp_dict.values():
                for item in least:
                    values.remove(item)


def rangeVoting(values, tieBreak):
    """Function to return the winner which is the alternative that has the maximum sum of valuations, i.e., the maximum sum of numerical values in the xlsx file

    Args:
        values (file): worksheet corresponding to an xlsx file
        tieBreak (int, 'min', 'max'): determines the winner incase of a tie break 
        
    Returns:
        int : final winner of the voting rule
    """
    agent_dict = {}
    total = {}
    winner = list()
    for col in range(1, values.max_column + 1):
        total = 0
        key = col
        if key not in agent_dict.keys():
            agent_dict[key] = []
        for row in range(1, values.max_row + 1):
            total += values.cell(row, col).value
            agent_dict[key] = total

    winner = get_max_val(agent_dict)
    return tie_break(generatePreferences(values), tieBreak, winner)
    
    
def get_max_val (dictionary):
    """Function to get the winners with the maximum values

    Args:
        dictionary (dict): dictionary from which the winners are to be determined

    Returns:
        list : list of winners
    """
    winner_list = list()
    max_val = max(dictionary.items(), key=lambda x:x[1])
    for key, values in dictionary.items():
        if values == max_val[1]:
            winner_list.append(key)
    return winner_list


def tie_break(preferences, tieBreak, winner):
    """Function to be implemented in case of a tie break with three options:
        max: Among the possible winning alternatives, select the one with the highest number
        min: Among the possible winning alternatives, select the one with the lowest number
        agent i: Among the possible winning alternatives, select the one that agent  ranks the highest in preference ordering 

    Args:
        preferences (dict): preferences of alternatives of the agents
        tieBreak (int): 'max', 'min' or an agent
        winner (list): list of possible winners

    Raises:
        ValueError: To be displayed in case the entered tieBreak is not an agent

    Returns:
        int : winner of voting
    """
    if tieBreak == 'max':
        return max(winner)
    elif tieBreak == 'min':
        return min(winner)
    try:
        if tieBreak in preferences.keys():
            for values in preferences[tieBreak]:
                if values in winner:
                    return values
        else:
            raise ValueError
    except ValueError:
        print("Incorrect input")