#python -m pip install tracery
# https://openbase.com/python/tracery/documentation
#git@github.com:headrotor/mastobots.git

# python program to reply to Mastodon mentions with a Captain
# Beefheart nickname. Call this repeatedly in crontab,
# for example, to run every 5 minutes:
# */5 * * * * /usr/bin/python3 /home/user/github/mastobots/bombdon.py >> ~/bombdon.log 2>&1

import tracery
import json
import os
from datetime import datetime
from tracery.modifiers import base_english


# pip3 install Mastodon.py
# https://mastodonpy.readthedocs.io/en/stable/
from mastodon import Mastodon
from mastodon import errors as Masto_errors

# first change to code directory so local files will be found 
os.chdir(os.path.dirname(os.path.abspath(__file__)))


verbose = False
masto_cred_file = 'bombdon_usercred.secret'
grammar_file = "dongrammar.json"

# test for existence of Mastodon API credential file    
if not os.path.isfile(masto_cred_file):
    print(f"Can't find Mastodon user credential file '{masto_cred_file}'")
    print(f"To register this app, see https://mastodonpy.readthedocs.io/en/stable")
    exit()

# load Tracery generative grammar file
with open(grammar_file, 'r') as gram_file:
    gram_data = json.load(gram_file)
    #print(gram_data)

grammar = tracery.Grammar(gram_data)
grammar.add_modifiers(base_english)

# Instantiate Mastodon API class instance 
# if we exceed rate limit, just quit and try again next time.
mastodon = Mastodon(access_token=masto_cred_file,
                    ratelimit_method='throw')

print(f"running at {datetime.now().isoformat()}")

# fetch notifications of anyone who mentioned us.
notis = mastodon.notifications(id=None,
                               account_id=None,
                               max_id=None,
                               min_id=None,
                               since_id=None,
                               limit=None,
                               exclude_types=None,
                               types=None,
                               mentions_only=True)

# for each notification, reply to the post "status" that mentioned us
for note in notis:
    if verbose:
        print(note)

    # create nickname from grammar
    nick = grammar.flatten("#origin#").strip()

    # display name of account that mentioned us
    display_name = note['account']['display_name']

    # id of this notification
    note_id = note['id']

    # id of the post that mentioned us
    status_id = note['status']['id']

    # text of the reply to the post that mentioned us
    status = f'Hello {display_name}, your Beefheart nickname is "{nick}"'
    
    # post reply
    try: 
        result = mastodon.status_reply(note['status'],
                                       status,
                                       in_reply_to_id=status_id,
                                       media_ids=None,
                                       sensitive=False,
                                       visibility=None,
                                       spoiler_text=None,
                                       language=None,
                                       idempotency_key=None,
                                       content_type=None,
                                       scheduled_at=None,
                                       poll=None,
                                       untag=True)

    except Masto_errors.MastodonNotFoundError:
        print("oops, can't find original status. Deleted?")

    print(f'replied "{status}"')
    if verbose:
        print("status")
    #mastodon.notifications_dismiss(note['id'])

mastodon.notifications_clear()
