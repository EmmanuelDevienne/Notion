import os
import argparse
import requests
import json
from time import sleep
from dotenv import load_dotenv

load_dotenv()

HEADERS = {
    "Authorization": "",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}


def read_database(database_id, propertie, headers):
    list_entry = []
    url = f"https://api.notion.com/v1/databases/{database_id}/query"

    page_count = 1
    request = requests.request("POST", url, headers=headers).json()

    content = request['results']

    while request['has_more']:
        page_count += 1

        request = requests.post(url, json={"start_cursor": request["next_cursor"]}, headers=headers).json()
        content.extend(request['results'])

    for data in content:
        raw_id = data['id']
        clean_id = "".join([d for d in raw_id if d not in "-"])

        properties = data['properties']
        title_list = properties.get(f'{propertie}', {}).get('title', [])
        name = title_list[0]['plain_text'] if title_list else ''

        list_entry.append((name, clean_id))

    return list_entry


def update_database(headers, payload):
    url = f'https://api.notion.com/v1/pages'
    requests.post(url, headers=headers, data=json.dumps(payload))


def upload_to_database(file_path, database_id, property_name, notion_token):
    HEADERS["Authorization"] = f"Bearer {notion_token}"

    with open(file_path, 'r') as file:
        lines = file.readlines()

    targets_payloads = []
    for line in lines:
        content = line.strip().split(" ")[0]
        targets_payload = {
            "parent": {
                "database_id": f"{database_id}"
            },
            "properties": {
                f"{property_name}": {
                    "title": [
                        {
                            "text": {
                                "content": f"{content}"
                            }
                        }
                    ]
                }
            }
        }
        targets_payloads.append(targets_payload)

    for payload in targets_payloads:
        update_database(HEADERS, payload)
        sleep(0.10)


def download_from_database(file_path, database_id, property_name, notion_token):
    HEADERS["Authorization"] = f"Bearer {notion_token}"

    entries = read_database(database_id, property_name, HEADERS)

    with open(file_path, 'w') as file:
        for entry in entries:
            content, _ = entry
            file.write(f"{content}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload/Download data to/from Notion database")
    parser.add_argument('-u', '--upload', action='store_true', help='Upload data from a file to Notion database')
    parser.add_argument('-d', '--download', action='store_true', help='Download data from Notion database to a file')
    parser.add_argument('-f', '--file', type=str, required=True, help='File path for upload/download')
    parser.add_argument('-id', '--database_id', type=str, required=True, help='Notion database ID')
    parser.add_argument('-p', '--property', type=str, required=True, help='Notion database property name')
    parser.add_argument('-t', '--token', type=str, required=True, help='Token name in .env file')

    args = parser.parse_args()

    notion_token = os.environ.get(args.token)
    if not notion_token:
        print(f"Token '{args.token}' not found in .env file.")
        exit(1)

    if args.upload:
        upload_to_database(args.file, args.database_id, args.property, notion_token)
    elif args.download:
        download_from_database(args.file, args.database_id, args.property, notion_token)
