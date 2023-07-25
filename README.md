# Notion Manager

The Notion Manager project is a command-line tool that allows you to populate a Notion database from a list in a local file and download a list from an existing Notion database.

## Prerequisites
Before using Notion Manager, you need to create a Notion integration, as it requires an integration token to interact with the Notion API.  
You can follow the official Notion API documentation :  [Notion Integration](https://developers.notion.com/docs/create-a-notion-integration).

## Installation

To use Notion Manager, please install the required dependencies by running the following command:

`pip install -r requirements.txt`

## Setup
Rename the `.env_example` file in the project directory to `.env`

Open the `.env` file using a text editor.

Add your Notion integration token(s) to the file.  
If you have multiple Notion workspaces, you can specify the token(s) for each workspace as follows:

```
Token_01=your_notion_token_for_workspace_1
Token_02=your_notion_token_for_workspace_2
```
Replace `Token_01`, `Token_02`, etc. with meaningful names for your tokens.

## Usage

`python DB_manager.py -d -f /path/to/local_file.txt -id <DATABASE_ID> -p <PROPERTY_NAME> -t <TOKEN_NAME>`

Available options:
- `-d` or `--download`: Downloads data from Notion to the specified local file 
- `-u` or `--upload`: Upload data from the specified local file to Notion.
- `-f` or `--file`: Path to the local file where the downloaded data will be saved.
- `-id` or `--database-id`: ID of the Notion database to synchronize.
- `-p` or `--property`: Name of the property in the Notion database that contains the data to download.
- `-t` or `--token`: Notion authentication token to access the database. If you have multiple Notion workspaces, please specify the token name corresponding to the workspace you want to use.



### Notion Database ID

The Notion database ID is a unique identifier that uniquely identifies the database. You can retrieve the ID of a Notion database from the URL when viewing it on the Notion site.

For example, if the database URL is `https://www.notion.so/myworkspace/a8aec43384f447ed84390e8e42c2e089?v=...`, then the ID of this database is `a8aec43384f447ed84390e8e42c2e089`.

## Disclaimer

This project is provided as is, without any warranty of any kind. The use of this project is at your own risk.

Feel free to open an issue if you encounter any problems or have any suggestions for improvement!
