import requests
import json
import logging
import socket

HOST = '0.0.0.0'
PORT = 7397


def jira_events():
    headers = {
        'Authorization': 'Basic <API_key>',
        'Content-Type': 'application/json',
    }
    logging.basicConfig(level=logging.INFO, filename='jira_audit.log', format='%(asctime)s %(levelname)s:%(message)s')
    response = requests.get('https://jira_address:8090/rest/api/2/auditing/record?limit=1000', headers=headers)

    text0 = json.loads(response.text)

    list_events = []
    for k in text0['records']:
        list_data = []
        with open("jira_audit.log", 'r') as f:
            data = f.read()
            if k["created"] in data:
                continue
            elif k['summary'] == 'Audit Log search performed':
                continue
            else:
                if 'summary' in k:
                    summary = ["name_event", k['summary']]
                    list_data.extend(summary)
                else:
                    summary = ["name_event", 'None']
                    list_data.extend(summary)
                if 'remoteAddress' in k:
                    remote = ["remoteAddress", k['remoteAddress']]
                    list_data.extend(remote)
                else:
                    remote = ["remoteAddress", 'None']
                    list_data.extend(remote)
                if 'authorKey' in k:
                    authorKey = ['authorKey', k['authorKey']]
                    list_data.extend(authorKey)
                else:
                    authorKey = ["authorKey", 'None']
                    list_data.extend(authorKey)
                if 'created' in k:
                    created = ["created", k['created']]
                    list_data.extend(created)
                else:
                    created = ["created", 'None']
                    list_data.extend(created)
                if 'category' in k:
                    category = ["category", k['category']]
                    list_data.extend(category)
                else:
                    category = ["category", 'None']
                    list_data.extend(category)
                if 'eventSource' in k:
                    eventSource = ["eventSource", k['eventSource']]
                    list_data.extend(eventSource)
                else:
                    eventSource = ["eventSource", 'None']
                    list_data.extend(eventSource)
                if 'objectItem' in k:
                    objectItem = ["objectItem", "name", k['objectItem']['name'],
                                  "typeName", k['objectItem']['typeName']]
                    list_data.extend(objectItem)
                else:
                    objectItem = ["objectItem", 'None']
                    list_data.extend(objectItem)
                if 'associatedItems' in k:
                    for kk in k['associatedItems']:
                        if 'id' in kk:
                            associatedItems = ["associatedItems", 'id', kk['id'], 'name', kk['name'],
                                           'typeName', kk['typeName']]
                            list_data.extend(associatedItems)
                        else:
                            associatedItems = ["associatedItems", 'id', "None", 'name', kk['name'],
                                               'typeName', kk['typeName']]
                            list_data.extend(associatedItems)
                else:
                    associatedItems = ["associatedItems", 'None']
                    list_data.extend(associatedItems)
                if 'changedValues' in k:
                    for kk in k['changedValues']:
                        if 'changedFrom' in kk:
                            if  'changedTo' in kk:
                                changedValues = ["changedValues", 'fieldName', kk['fieldName'], 'changedFrom', kk['changedFrom'],
                                         'changedTo', kk['changedTo']]
                                list_data.extend(changedValues)
                        elif 'changedFrom' in kk:
                            changedValues = ["changedValues", 'fieldName', kk['fieldName'], 'changedFrom',
                                             kk['changedFrom'],
                                             'changedTo', "None"]
                            list_data.extend(changedValues)
                        elif 'changedTo' in kk:
                            changedValues = ["changedValues", 'fieldName', kk['fieldName'], 'changedFrom',
                                             "None",
                                             'changedTo', kk['changedTo']]
                            list_data.extend(changedValues)
                        else:
                            changedValues = ["changedValues", 'fieldName', kk['fieldName'], 'changedFrom',
                                             "None",
                                             'changedTo', "None"]
                            list_data.extend(changedValues)
                else:
                    changedValues = ["changedValues", 'None']
                    list_data.extend(changedValues)

                logging.info(list_data)

                list_events.append(list_data)

    with open('jira_audit.log', 'rb') as file:
        data3 = file.read()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(data3)
jira_events()
# print(list_events)
# for list in list_events:
#     print(list)
# print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))