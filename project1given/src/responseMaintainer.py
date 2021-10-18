import datetime

def responseMaintainer(issues):
    if issues is None:
        return 0.0
    num_issues = issues.shape[0]
    if num_issues == 0:
        return 0.0
    open_issues = 0
    close_issues = 0
    response_score = 0
    for i in range(issues.shape[0]):
        dict_row = issues.iloc[i]
        datetime_create = datetime.datetime.strptime(dict_row['created_at'], '%Y-%m-%dT%H:%M:%SZ')
        datetime_update = datetime.datetime.strptime(dict_row['updated_at'], '%Y-%m-%dT%H:%M:%SZ')
        if datetime_create == datetime_update:
            response_score += 1
        if dict_row['state'] == 'open':
            open_issues += 1
        else:
            close_issues += 1
    ratio_open_close = close_issues/open_issues
    return 0.1 * ratio_open_close + ((response_score/num_issues) *0.9) 