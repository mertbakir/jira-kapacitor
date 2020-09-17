import json
import sys
from collections import Counter
from jira import JIRA

def getLabelsFromTags(tags):
  labels = ''
  for value in tags.values():
    labels += ''+ value + ','

  if len(labels) > 2:
    return(labels[:-1]).split(',')
  else:
      return

auth = ("username", "password")
jira_url = "https://smartdesk.thyteknik.com.tr"

## Sample Data.
sampleOutput = r"""{"id":"JIRA_TEST:system:host=SAWPGITLAB","message":"[CRITICAL] JIRA is 0.87 on SAWPGITLAB.","details":"\n\u003cb\u003eHost:\u003c/b\u003e SAWPGITLAB \u003cbr\u003e\n\u003cb\u003eCore:\u003c/b\u003e 2 \u003cbr\u003e\n\u003cb\u003eLoad 1:\u003c/b\u003e 0.87 \u003cbr\u003e\n\u003cb\u003eLoad 5:\u003c/b\u003e 0.52 \u003cbr\u003e\n\u003cb\u003eLoad 15:\u003c/b\u003e 0.61 \u003cbr\u003e\n\u003chr\u003e\n\u003cb\u003eAlert Time:\u003c/b\u003e Tue, Aug 25 2020 at 15:36:25 \u0026#43;03 \u003cbr\u003e\n\u003cb\u003eState Duration:\u003c/b\u003e 0s \u003cbr\u003e\n\u003cb\u003eGo To Dashboard:\u003c/b\u003e \u003ca href=\"https://grafana.thyteknik.com.tr/d/7yqxqfSWk/linux-system-details?var-host=SAWPGITLAB\"\u003e\nSAWPGITLAB Linux Server\u003c/a\u003e\n","time":"2020-08-25T12:36:25Z","duration":0,"level":"CRITICAL","data":{"series":[{"name":"system","tags":{"host":"SAWPGITLAB","os":"linux"},"columns":["time","load1","load15","load5","n_cpus","value"],"values":[["2020-08-25T12:36:25Z",0.87,0.61,0.52,2,0.435]]}]},"previousLevel":"OK","recoverable":true}"""
alertJson = json.loads(sampleOutput)
category = "MARMARA" # Only static tag.
alertID = alertJson.get("id")
tags = alertJson.get("data").get("series")[0].get("tags")
hostname = tags.get("host")
message = alertJson.get("message")
details = alertJson.get("details")

## JIRA

issue_dict = {
    'project': {'id': 10115},
    'issuetype': {'name': 'Incident'},
    'labels' :getLabelsFromTags(tags),
    'summary': message,
    'description': details,
    'customfield_15701': category,
    'customfield_13803': hostname,
    #'customfield_15800': "2015-07-03T14:08:00.000-0500", #Alert Time
    'customfield_10202': 'ym/7814c0b4-bec4-4880-8b66-3cd7184f17d5'
}

jira = JIRA(server = jira_url, options={'verify':False}, basic_auth = auth)
new_issue = jira.create_issue(fields=issue_dict)