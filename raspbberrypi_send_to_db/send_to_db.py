import asyncio
from azure.eventhub.aio import EventHubConsumerClient
from azure.eventhub.extensions.checkpointstoreblobaio import BlobCheckpointStore
import os
from dotenv import load_dotenv
from azure.cosmos import cosmos_client
import json

load_dotenv()

connection_str = os.getenv("CONNECTION_STRING")
consumer_group = os.getenv("CONSUMER_GROUP")
eventhub_name = os.getenv("EVENTHUB_NAME")
checkpoint_db = os.getenv("CHECKPOINT_DB")
checkpoint_db_name = os.getenv("CHECKPOINT_DB_NAME")

CONFIG = {
    "ENDPOINT": os.getenv("COSMOSDBB_ENDPOINT"),
    "PRIMARYKEY": os.getenv("COSMOSDB_PRIMARYKEY"),
    "DATABASE": os.getenv("COSMOSDB_TEST"),
    "CONTAINER": os.getenv("COSMOSDBB_CONTAINER")
}

CONTAINER_LINK = f"dbs/{CONFIG['DATABASE']}/colls/{CONFIG['CONTAINER']}"
FEEDOPTIONS = {}
FEEDOPTIONS["enableCrossPartitionQuery"] = True

QUERY = {
    "query": f"SELECT * from c"
}

client = cosmos_client.CosmosClient(CONFIG["ENDPOINT"], {"masterKey": CONFIG["PRIMARYKEY"]})
db = client.get_database_client(CONFIG["DATABASE"])
container = db.get_container_client(CONFIG["CONTAINER"])

async def on_event(partition_context, event):
    data = event.body_as_str(encoding='UTF-8').strip()
    data_list = data.split(',')
    data_list_dict = {}
    for item in data_list:
        (k,v) = item.split(":")
        data_list_dict[k] = v

    item_id = ""
    for item in container.query_items(
        query='SELECT * FROM c',
        enable_cross_partition_query=True):
        print(json.dumps(item, indent=True))
        item_id = item["id"]

    container.upsert_item({
                'id': item_id,
                "Temperature": data_list_dict["Temperature"],
                "Humidity": data_list_dict["Humidity"],
                "Light": data_list_dict["Light"]
                }
        )
    await partition_context.update_checkpoint(event)

async def main():
    # Create an Azure blob checkpoint store to store the checkpoints.
    checkpoint_store = BlobCheckpointStore.from_connection_string(checkpoint_db, checkpoint_db_name)
    client = EventHubConsumerClient.from_connection_string(connection_str, consumer_group=consumer_group, eventhub_name=eventhub_name, checkpoint_store=checkpoint_store)


    async with client:
        # Call the receive method. Read from the beginning of the partition (starting_position: "-1")
        await client.receive(on_event=on_event)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    # Run the main method.
    loop.run_until_complete(main())   