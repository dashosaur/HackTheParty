import asyncio
import uuid
from hack_points import award_hack_points

async def main():
    await award_hack_points(782868967881441321, 'allans_test_event', 1, uuid.uuid4(), 'allans_test_bot')

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
