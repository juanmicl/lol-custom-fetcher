from lcuapi import LCU, Event, EventProcessor
import requests, json

# EventProcessors are classes that handle/process different events.
# Create an EventProcessor by inherenting from the EventProcessor class.
# You then have to define two methods, "can_handle" and "handle".
class PrintSomeEventInfo(EventProcessor):

    # The "can_handle" method must return True and False.
    # Return True if this event handler can handle the event. Return False if not.
    def can_handle(self, event: Event):        
        if issubclass(event.__class__, Event):
            return True
        else:
            return False

    # The "handle" method defines the functionality of the handler.
    # This is where you write code to do something with the event.
    # In this example, I simply print out the URI of the event and the time at which it was created.
    # The only other attribute of an Event is: "event.data".
    def handle(self, event: Event):
        print(f"Event<uri={event.uri} created={event.created}>")


def main():
    lcu = LCU()

    lcu.attach_event_processor(PrintSomeEventInfo())

    lcu.wait_for_client_to_open()
    lcu.wait_for_login()

    partidas_historial = lcu.get('/lol-match-history/v2/matchlist?begIndex=0&endIndex=10')
    partidas_historial_custom = partidas_historial['games']['games']

    game_ids = []

    for game in partidas_historial_custom:
        if game['gameType'] == 'CUSTOM_GAME':
            game_ids.append(game['gameId'])

    for game_id in game_ids:
        game_data = lcu.get(f"/lol-match-history/v1/games/{game_id}")
        print(f'[i] Enviando Partida -> {game_data["gameCreationDate"]}')
        requests.request(
            "POST",
            'https://yourwebsite.com/callback/custom-games',
            data = json.dumps(game_data)
        )

if __name__ == '__main__':
    main()
