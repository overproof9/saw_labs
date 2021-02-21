import os
import errno

LOG_PATH = '../logs/action_log.txt'

def write_log(data):
    created = False
    if not os.path.exists(os.path.dirname(LOG_PATH)):
        try:
            os.makedirs(os.path.dirname(LOG_PATH))
            created = True
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
    with open(LOG_PATH, 'a') as f:
        if created:
            f.write('#header\n#DateTime\t\t\t\tIP\tTARGET URL\tSESSION COOKIES\t\t\t\t\tUSER ID\tROLE ID\tMETHOD\tPAYLAOD\n\n')
        for value in data.values():
            f.write(f'{value}\t')
        f.write('\n\r')
    return True