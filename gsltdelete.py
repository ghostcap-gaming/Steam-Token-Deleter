import requests
from datetime import timedelta, datetime

TIMEOUT = timedelta(minutes=130)
ACCOUNT_LIST_ENDPOINT_URL = 'https://api.steampowered.com/IGameServersService/GetAccountList/v1'
DELETE_ACCOUNT_ENDPOINT_URL = 'https://api.steampowered.com/IGameServersService/DeleteAccount/v1/'
REQUEST_DATA = {'key': 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'}
  
def delete_account(account_steamid: str):
    request = requests.post(
        url=DELETE_ACCOUNT_ENDPOINT_URL,
        params=REQUEST_DATA | {'steamid': account_steamid}
    )

    if request.status_code != 200:
        raise Exception(f'Request failed with status code: {request.status_code}')

    print(f'Account {account_steamid} deleted due to timeout')

def get_accounts():
    request = requests.get(
        url=ACCOUNT_LIST_ENDPOINT_URL,
        params=REQUEST_DATA
    )

    if request.status_code != 200:
        raise Exception(f'Request failed with status code: {request.status_code}')

    response = request.json()['response']

    return response['servers'] if 'servers' in response else []

def delete_accounts_with_old_tokens(timeout: timedelta):
    accounts = get_accounts()

    for account in accounts:
        last_logon = datetime.fromtimestamp(account['rt_last_logon'])

        print(f'steamid: {account["steamid"]}, Last logon: {last_logon}, Expiration: {last_logon + timeout}')
        
        if last_logon + timeout < datetime.now():
            delete_account(account['steamid'])

def main():
    delete_accounts_with_old_tokens(TIMEOUT)

if __name__ == '__main__':
    main()