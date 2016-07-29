import json
import time

from twilio.rest import TwilioRestClient

from _db_logic import connect_db
from _db_logic import DATA
from _db_logic import LURE_DATA
from server import Pokemon


notified_pokemon = []


with open('config.json') as config:
    config = json.load(config)
    twilio_info = config['twilio_info']


with open('pokemon.en.json') as pokemon_names_file:
    pokemon_names = {
        int(k): v for k, v in json.load(pokemon_names_file).items()
    }


def send_notification(pokemon):
    client = TwilioRestClient(
        twilio_info['account_sid'],
        twilio_info['auth_token'],
    )
    client.messages.create(
        to=twilio_info['to_number'],
        from_=twilio_info['from_number'],
        body='{name} spawned nearby and disappears at {expires}!'.format(
            name=pokemon.name,
            expires=pokemon.expires_at_formatted,
        ),
    )


def get_pokemon(db):
    current_time_ms = time.time() * 1000

    # Get spawend
    data = DATA.select_non_expired(db, current_time_ms)
    lure_data = LURE_DATA.select_non_expired(db, current_time_ms)
    spawned_pokemon = [Pokemon(*row) for row in data + lure_data]

    # Get expired
    data = DATA.select_recently_expired(db, current_time_ms)
    lure_data = LURE_DATA.select_recently_expired(db, current_time_ms)
    expired_pokemon = [Pokemon(*row) for row in data + lure_data]

    return (spawned_pokemon, expired_pokemon,)


def notify_pokemon(spawned_pokemon):
    for pokemon in spawned_pokemon:
        if (
            pokemon.name.lower() in twilio_info['notify'] and
            pokemon.spawn_id not in notified_pokemon
        ):
            send_notification(pokemon)
            notified_pokemon.append(pokemon.spawn_id)


def clear_from_cache(expired_pokemon):
    for pokemon in expired_pokemon:
        if pokemon.spawn_id in notified_pokemon:
            notified_pokemon.remove(pokemon.spawn_id)


def main():
    with connect_db() as db:
        while True:
            spawned_pokemon, expired_pokemon = get_pokemon(db)
            notify_pokemon(spawned_pokemon)
            clear_from_cache(expired_pokemon)
            time.sleep(1)


if __name__ == '__main__':
    exit(main())
