import aiohttp

# Hack event - POST /hack-api/v1/collection/hack_event
# user: snowflake (id)
# event_name: string (displayed to users)
# points: int
# uuid: uuid (optional, to allow for idempotency/replay. auto generated if missing)
# bot_name: str
# metadata: json

hack_api_url = 'https://us-central1-public-house-virtual-mansion.cloudfunctions.net/hack-api/v1/collection/hack_event'

async def award_hack_points(snowflake, event_name, points, uuid, bot_name):
    print(f"Awarding {points} points to {snowflake}/{event_name}/{bot_name}")

    data = {
        'user': snowflake,
        'event_name': event_name,
        'points': points,
        'uuid': uuid,
        'bot_name': bot_name,
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(hack_api_url, data = data) as response:
            body = await response.text()
            print(f"Response for {snowflake}/{event_name}/{bot_name}: {response.status} {response.headers['content-type']} {body}")
