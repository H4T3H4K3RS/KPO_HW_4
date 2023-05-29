import time
import requests
import os

# Get the base URL from the environment variable 'DOMAIN', defaulting to 'http://127.0.0.1:8000/api/'
BASE_URL = os.getenv("DOMAIN", "http://127.0.0.1:8000/api/")

# Create a session and set the authorization header with the bot secret
session = requests.session()
session.headers['Authorization'] = f'{os.getenv("BOT_SECRET", "bot_secret")}'


def process_order(order_id: int):
    """
    Process an order by calling the 'process' action endpoint for a specific order.

    Args:
        order_id (int): The ID of the order to be processed.
    """
    url = f'{BASE_URL}orders/{order_id}/process/'
    response = session.post(url)

    if response.status_code != 200:
        print(f'Error processing order {order_id}: {response.text}')


def process_orders():
    """
    Retrieve and process pending orders.

    This function retrieves the list of pending orders from the API and processes each order by calling the 'process'
    action endpoint.
    """
    url = f'{BASE_URL}orders/'
    response = session.get(url, params={'status': 'pending'})

    if response.status_code == 200:
        orders = response.json()
        print(f"Pending orders: [{len(orders)}]")
        for order in orders:
            if order['status'] != 'pending':
                continue
            order_id = order['id']
            process_order(order_id)
    else:
        print(f'Error retrieving orders: {response.text}')


def main():
    while True:
        process_orders()
        time.sleep(1)


if __name__ == '__main__':
    main()
