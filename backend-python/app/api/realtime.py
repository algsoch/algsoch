"""WebSocket and SSE endpoints for real-time features."""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import StreamingResponse
import json
import asyncio
from datetime import datetime
from typing import List
import time

from app.services.activity import add_connection, remove_connection

router = APIRouter(tags=["realtime"])

# WebSocket connections
ws_connections: List[WebSocket] = []

# Server start time for uptime calculation
server_start_time = time.time()


@router.websocket("/ws/live")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time metrics."""
    await websocket.accept()
    ws_connections.append(websocket)
    
    try:
        while True:
            # Send metrics every 2 seconds
            uptime = int(time.time() - server_start_time)
            active_clients = len(ws_connections)
            
            data = {
                "type": "metrics",
                "timestamp": datetime.utcnow().isoformat(),
                "payload": {
                    "uptime": uptime,
                    "active_clients": active_clients,
                    "version": "1.0.0",
                    "ping": "ok"
                }
            }
            
            await websocket.send_json(data)
            await asyncio.sleep(2)
            
    except WebSocketDisconnect:
        ws_connections.remove(websocket)
    except Exception as e:
        if websocket in ws_connections:
            ws_connections.remove(websocket)


@router.get("/stream/activity")
async def stream_activity(request: Request):
    """Server-Sent Events endpoint for activity stream."""
    
    async def event_generator():
        queue = asyncio.Queue()
        await add_connection(queue)
        
        try:
            while True:
                # Check if client disconnected
                if await request.is_disconnected():
                    break
                
                # Wait for new activity with timeout
                try:
                    activity = await asyncio.wait_for(queue.get(), timeout=30.0)
                    yield f"data: {json.dumps(activity)}\n\n"
                except asyncio.TimeoutError:
                    # Send heartbeat
                    yield f": heartbeat\n\n"
                    
        except asyncio.CancelledError:
            pass
        finally:
            await remove_connection(queue)
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        }
    )


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "uptime": int(time.time() - server_start_time),
        "active_ws_connections": len(ws_connections),
    }
