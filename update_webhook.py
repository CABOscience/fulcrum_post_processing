#!/usr/bin/env python
import parameters as PA
import tools as TO
import logs as LO
import tools_fulcrum_api as TOFA
import sys, time

'''
Usage:
python update_webhook.py [-h] [-a FulcrumApiKey] 

Options Fulcrum Backup.
optional arguments:
  -a FulcrumApiKey, --FulcrumApiKey FulcrumApiKey
                        Need a fulcrum Api key
'''
##############################################
# MAIN FUNCTION
##############################################
def main():
  PA.set_parameters()
  LO.create_log("webhook")
  webhook = TOFA.get_webhook_status(PA.WebhookID)
  for k in webhook.keys():
    print(k)
    print(webhook[k])

  #for att in dir(webhook):
  #  print (att, getattr(webhook,att))
  if not webhook["webhook"]['active']:
    obj = {
      "webhook": {
        "name": webhook["webhook"]["name"],
        "url": webhook["webhook"]["url"],
        "active": True
      }
    }
    TOFA.fulcrum_update_webhook(PA.WebhookID,obj)

##############################################
# MAIN
##############################################
if __name__ == '__main__':
  main ()

