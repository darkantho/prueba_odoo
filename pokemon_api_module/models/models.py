# models/pokemon.py
from odoo import models, fields, api
import requests
import collections
from collections import namedtuple


class Pokemon(models.Model):
    _name = 'pokemon'
    _description = 'Pokemon Model API'

    name = fields.Char(string='Name')
    height = fields.Integer(string='Height')
    weight = fields.Integer(string='Weight')
    moves_ids = fields.One2many('pokemon.moves', 'pokemon_id', string='Habilites')
    type_ids = fields.One2many('pokemon.type', 'pokemon_id', string='Types')
    stats_ids = fields.One2many('pokemon.stats', 'pokemon_id', string='Stats')
    


    @api.model
    def fetch_pokemon_data(self):
        total_pokemon = self.env['pokemon'].search_count([])
        url = f'https://pokeapi.co/api/v2/pokemon?limit=20&offset={total_pokemon}'
        print(url)
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            pokemon = namedtuple('Pokemon', ['name', 'url'])
            pokemons = list(map(pokemon._make, [(result['name'], result['url']) for result in data['results']]))
            for poke in pokemons:
                pokemon_data = requests.get(poke.url).json()
                moves = pokemon_data['moves']
                types = pokemon_data['types']
                stats = pokemon_data['stats']
              
                self.create({
                    'name': poke.name,
                    'height': pokemon_data['height'],
                    'weight': pokemon_data['weight'],
                    'moves_ids': [(0,0,{'name':move['move']['name'],'url': move['move']['url']}) for move in moves],
                    'type_ids': [(0, 0, {'name': type['type']['name'], 'url': type['type']['url']}) for type in types],
                    'stats_ids': [(0,0,{'name': stat['stat']['name'],'base_stat': stat['base_stat'], 'effort': stat['effort']}) for stat in stats ],
                })            
            # for result in data['results']:
            #     pokemon_name = result['name']
            #     pokemon_url = result['url']
            #     pokemon_data = requests.get(pokemon_url).json()
            #     self.create({
            #         'name': pokemon_name,
            #         'height': pokemon_data['height'],
            #         'weight': pokemon_data['weight'],
            #     })
        

class moves(models.Model):
    _name = 'pokemon.moves'
    _description = 'Habilites Model API'

    name = fields.Char(string='Name')
    url = fields.Char(string='URL')
    pokemon_id = fields.Many2one('pokemon', string='Pokemon')

    @api.model
    def fetch_habilites_data(self):
        url = 'https://pokeapi.co/api/v2/ability/'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            for result in data['results']:
                habilites_name = result['name']
                habilites_url = result['url']
                habilites_data = requests.get(habilites_url).json()
                self.create({
                    'name': habilites_name,
                    'effect': habilites_data['effect_entries'][0]['effect'],
                    'pokemon_id': habilites_data['pokemon']['name'],
                })

class PokemonType(models.Model):
    _name = 'pokemon.type'
    _description = 'Pokemon Type Model API'

    name = fields.Char(string='Name')
    url = fields.Char(string='url')
    pokemon_id = fields.Many2one('pokemon', string='Pokemon')

    @api.model
    def fetch_pokemon_type_data(self):
        url = 'https://pokeapi.co/api/v2/type/'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            for result in data['results']:
                type_name = result['name']
                type_url = result['url']
                type_data = requests.get(type_url).json()
                self.create({
                    'name': type_name,
                    'pokemon_id': type_data['pokemon']['name'],
                })

class PokemonStats(models.Model):
    _name = 'pokemon.stats'
    _description = 'Pokemon Stats Model API'

    name = fields.Char(string='Name')
    base_stat = fields.Integer(string='Base Stat')
    effort = fields.Integer(string='Effort')
    pokemon_id = fields.Many2one('pokemon', string='Pokemon')

    @api.model
    def fetch_pokemon_stats_data(self):
        url = 'https://pokeapi.co/api/v2/stat/'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            for result in data['results']:
                stats_name = result['name']
                stats_url = result['url']
                stats_data = requests.get(stats_url).json()
                self.create({
                    'name': stats_name,
                    'base_stat': stats_data['base_stat'],
                    'effort': stats_data['effort'],
                    'pokemon_id': stats_data['pokemon']['name'],
                })