from data_processing.channel_extractor import extract_channel_data

channel_id = "UC_x5XG1OV2P6uZZ5FSM9Ttw"

df = extract_channel_data(channel_id)

print(df)
