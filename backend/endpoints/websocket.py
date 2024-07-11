from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

from backend import deps, schemas
from backend.services import notification

router = APIRouter()
router.tags = ["html page for ws"]


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    is_superuser: bool = Depends(deps.is_superuser_socket),
):
    await websocket.accept()
    notification.add_connection(
        schemas.ConnectedUser(is_superuser=is_superuser, connection=websocket)
    )
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received message: {data}")
    except WebSocketDisconnect:
        notification.remove_connection(websocket)


@router.get("/")
async def get():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>WebSocket Notifications</title>
    </head>
    <body>
        <h1>WebSocket Notifications</h1>
        <ul id="notifications"></ul>
        <script>
            const ws = new WebSocket("ws://localhost:8000/api/ws");

            ws.onmessage = function(event) {
                const notifications = document.getElementById('notifications');
                const message = event.data;
                const li = document.createElement('li');
                li.textContent = message;
                notifications.appendChild(li);
            };

            ws.onopen = function(event) {
                ws.send("Client connected");
            };
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
