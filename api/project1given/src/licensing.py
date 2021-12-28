import json

def licensing(license, compatible_license):
    '''
    License score:
    Calculates License score based on license compatibility with LGPLv2.1
    License score will either be 1 or 0
    1 if compatible, 0 if not
    '''
    #comaptible license are in spdx_id
    if license == None:
        return 0
    elif license in compatible_license.keys():
        return 1.0
    else:
        return 0.0