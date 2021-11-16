
def busFactor(contributors):
    '''
    Bus Factor Score
    The number of maintainers 

    the score is calculated with ((n-1)/n) this is because the bus factor score should measure how much the project will be affected if one person left the team 
    '''
    if contributors >= 100:
        return 1.0
    else:
        n = contributors
        score = ((n-1)/n)
        return score