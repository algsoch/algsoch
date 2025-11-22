"""Activity broadcast service for SSE."""
import asyncio
import json
from datetime import datetime
from typing import Dict, Any, List
from asyncio import Queue

# Active SSE connections
active_connections: List[Queue] = []


async def broadcast_activity(activity: Dict[str, Any]) -> None:
    """Broadcast activity to all SSE connections."""
    activity["timestamp"] = datetime.utcnow().isoformat()
    
    # Remove disconnected queues
    disconnected = []
    for queue in active_connections:
        try:
            queue.put_nowait(activity)
        except:
            disconnected.append(queue)
    
    for queue in disconnected:
        active_connections.remove(queue)


async def add_connection(queue: Queue) -> None:
    """Add a new SSE connection."""
    active_connections.append(queue)


async def remove_connection(queue: Queue) -> None:
    """Remove an SSE connection."""
    if queue in active_connections:
        active_connections.remove(queue)
