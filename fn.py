import os
import os.path
import json
import git
from datetime import datetime

import cloudpassage

def get_all_policies(session, savepath):

    csm = cloudpassage.ConfigurationPolicy(session)
    fim = cloudpassage.FimPolicy(session)
    fw = cloudpassage.FirewallPolicy(session)
    lids = cloudpassage.LidsPolicy(session)
    special_events = cloudpassage.SpecialEventsPolicy(session)

    for policy in csm.list_all():
        policy_detail = csm.describe(policy['id'])
        filename = policy_detail['name'] + ".json"
        path = savepath + "/csm"
        completename = os.path.join(path, filename)
        try:
            with open(completename, 'w') as outfile:
                outfile.write(json.dumps(policy_detail, indent=2))
        except FileNotFoundError:
            pass

    for policy in fim.list_all():
        policy_detail = fim.describe(policy['id'])
        filename = policy_detail['name'] + ".json"
        path = savepath + "/fim"
        completename = os.path.join(path, filename)
        try:
            with open(completename, 'w') as outfile:
                outfile.write(json.dumps(policy_detail, indent=2))
        except FileNotFoundError:
            pass

    for policy in fw.list_all():
        policy_detail = fw.describe(policy['id'])
        filename = policy_detail['name'] + ".json"
        path = savepath + "/firewall"
        completename = os.path.join(path, filename)
        try:
            with open(completename, 'w') as outfile:
                outfile.write(json.dumps(policy_detail, indent=2))
        except FileNotFoundError:
            pass

    for policy in lids.list_all():
        policy_detail = lids.describe(policy['id'])
        filename = policy_detail['name'] + ".json"
        path = savepath + "/lids"
        completename = os.path.join(path, filename)
        try:
            with open(completename, 'w') as outfile:
                outfile.write(json.dumps(policy_detail, indent=2))
        except FileNotFoundError:
            pass

    for policy in special_events.list_all():
        policy_detail = special_events.describe(policy['id'])
        filename = policy_detail['name'] + ".json"
        path = savepath + "/special_events"
        completename = os.path.join(path, filename)
        try:
            with open(completename, 'w') as outfile:
                outfile.write(json.dumps(policy_detail, indent=2))
        except FileNotFoundError:
            pass

def localcommit(savepath):
    result = True
    # Write policies to disk
    path_csm = savepath + "/csm"
    path_fim = savepath + "/fim"
    path_fw = savepath + "/firewall"
    path_lids = savepath + "/lids"

    for file in os.listdir(path_csm):
        if os.stat(path_csm + "/" + file).st_size == 0:
            result = False
            print(file + " is empty")

    for file in os.listdir(path_fim):
        if os.stat(path_fim + "/" + file).st_size == 0:
            result = False
            print(file + " is empty")
    for file in os.listdir(path_fw):
        if os.stat(path_fw + "/" + file).st_size == 0:
            result = False
            print(file + "is empty")
    for file in os.listdir(path_lids):
        if os.stat(path_lids + "/" + file).st_size == 0:
            result = False
            print(file + " is empty")
    return result

def remotepush(gitrepo, repocomment):
    repo = git.Repo(gitrepo)
    # Make sure we have the lastest version
    repo.git.pull()
    repo.git.add('.')
    if len(repocomment) < 1:
        repo.git.commit(message= "back up at " + str(datetime.now()))
    else:
        repo.git.commit(message = repocomment)
    repo.git.push()
    result = repo.git.status()
    return result
