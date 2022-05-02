from flask import Flask
import tracery
import random, os, csv
import requests
from tracery.modifiers import base_english

def get_meme(data):
  meme_url = None

  params = {
    'username': 'FareedIdris',
    'password': os.environ['IMGFLIP_PASS'],
    'template_id': data['id']
  }

  for i, text in enumerate(data['boxes']):
    params[f"boxes[{i}][text]"] = text

  meme_resp = requests.post('https://api.imgflip.com/caption_image', data=params)
  meme_data = meme_resp.json()
  if meme_resp.ok and meme_data['success']:
    meme_url = meme_data['data']['url']

  return meme_url

nouns = [
  'you',
  'your money',
  'the crypto community',
  'the world',
  'financial freedom',
  'your finances',
  'your wallet'
]

def get_tweet(app: Flask):
  countries = []

  with open(os.path.join(app.root_path, 'countries.csv')) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
      countries.append(row[0])

  base_topics = ['Space', 'Energy']
  base_topic_locations = {
    'Space': ['the moon', 'mars', 'space', 'the future', 'jupiter', 'the milky way', 'andromeda', 'mercury', 'venus', 'earth', 'uranus', 'neptune', 'pluto', 'the sun'],
    'Energy': countries
  }

  base_topic = random.choice(base_topics)
  base_topic_location = random.choice(base_topic_locations[base_topic])

  project_name_rules = {
    'base_topic': base_topic,
    'origin': ['#base_topic##project_name_affix.capitalize#', '#project_name_affix.capitalize##base_topic#', '#prefix.capitalize##base_topic#', '#base_topic#-#project_name_affix.capitalize#', '#project_name_affix.capitalize#-#base_topic#', '#base_topic##project_name_affix.capitalize# #suffix.capitalize#', '#project_name_affix.capitalize##base_topic# #suffix.capitalize#', '#prefix.capitalize##base_topic# #suffix.capitalize#', '#base_topic#-#project_name_affix.capitalize# #suffix.capitalize#', '#project_name_affix.capitalize#-#base_topic# #suffix.capitalize#'],
    'prefix': ['doge', 'super', 'ultra', 'smart', 'the', 'cool', 'shiba', 'safe'],
    'project_name_affix': ['coin', "NFT", 'meta', 'crypto', 'games', 'rocket', 'safe', 'ape', 'chain', 'swap', 'token', 'dollar', 'fuel', 'network', 'gold', 'protocol', 'elon', 'net', 'AI'],
    'suffix': ['2.0', '2', 'next', 'ultra', 'max']
  }

  project_name_grammer = tracery.Grammar(project_name_rules)
  project_name_grammer.add_modifiers(base_english)
  project_name = project_name_grammer.flatten("#origin#")
  

  rules = {
    'base_topic': base_topic,
    'origin': [
      f'[main_crypto_term:#crypto_term.capitalize#]#main_crypto_term# + #base_topic# = #emoji#! {project_name} #is# #delivery# #main_crypto_term# to #location.capitalize#! See if you can keep #activity# without {project_name} in your life! \##crypto_term# \##location# #meme#',
      f"[main_emoji:#emoji#]Don't be #nouns#! {project_name} is the #time_adjective# #adjective# #thing#! Our #crypto_adjective#, #crypto_adjective# #platform# #empowered_origin#!!#main_emoji##main_emoji# \##location# \##crypto_term# \##crypto_term# \##crypto_term# #meme#",
    ],
    'thing': ['thing', 'project', 'adventure', 'status symbol', 'thing to have'],
    'is': ['is', 'will be', 'has been', 'has always been', 'can start', 'has started', 'will start'],
    'platform': ['platform', 'environment', 'website', 'network', 'exhange', 'token', 'coin', 'cryptocurrency', 'project'],
    'nouns': ['a #adjective# loser', 'a #adjective# winner', 'an #adjective# investor', 'left out', 'scared', 'afraid'],
    'time_adjective': ['next', 'current', 'oldest', 'previous', 'newest'],
    'adjective': ['big', 'small', 'fun', 'annoying', 'sad', 'traumatising', 'exciting', 'amazing', 'terrible'],
    'crypto_adjective': ['decentralized', 'open', 'free', 'blockchain-based', 'web 3.0', 'digital'],
    'delivery': ['bringing', 'delivering', 'introducing', 'taking', 'distributing'],
    'crypto_term': ['NFT', 'web3', 'web 3.0', 'blockchain', 'crypto', 'nft', 'bitcoin'],
    'emoji': ['😍', '🥰', '😇', '😭', '🥳', '🤩', '🤬', '🤯', '💩', '🤢', '🤮', '🤡', '💀', '🎯', '🚀', '❤️', '💔', '💪'],
    'empowered_origin': ['#is# #delivery# #solvable_nouns# to #location#', '#is# #delivery# #solvable_nouns# to #location#'],
    'solvable_nouns': ['renewable energy', 'wind energy', 'solar energy', 'online payments', 'tree farms'],
    'location': base_topic_location,
    'activity': ['running', 'smiling', 'jumping', 'jogging', 'waking up', 'living', 'dying', 'fishing', 'eating'],
    'drake_meme_top_text': [f'[#setActivity#]#main_activity# without owning {project_name}'],
    'drake_meme_bottom_text': [f'#main_activity# while owning {project_name}'],
    'setActivity': '[main_activity:#activity.capitalize#]',
  }

  grammar = tracery.Grammar(rules)
  grammar.add_modifiers(base_english)

  base_topic_memes = {
    'Space': [
      # get_meme({
      #   'id': 112126428,
      #   'name': 'Distracted Boyfriend',
      #   'boxes': [random.choice(base_topic_locations[base_topic]).upper(), random.choice(nouns).upper(), random.choice(nouns).upper()]
      # }),
      get_meme({
        'id': 181913649,
        'name': 'Drake Hotline Bling',
        'boxes': [grammar.flatten('#drake_meme_top_text#'), grammar.flatten('#drake_meme_bottom_text#')]
      }),
    ],
    'Energy': [
      # get_meme({
      #   'id': 112126428,
      #   'name': 'Distracted Boyfriend',
      #   'boxes': [random.choice(nouns).upper(), base_topic_location.upper(), random.choice(nouns).upper()]
      # }),
      get_meme({
        'id': 181913649,
        'name': 'Drake Hotline Bling',
        'boxes': [grammar.flatten('#drake_meme_top_text#'), grammar.flatten('#drake_meme_bottom_text#')]
      }),
    ]
  }

  grammar.push_rules('meme', base_topic_memes[base_topic])
  return grammar.flatten("#origin#")