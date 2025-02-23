from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
import json

from use_case.utils.jwt_handler import get_current_user
from config.components.logging_config import logger

active_connections = {}

signal_router = APIRouter()


@signal_router.websocket("/ws/signaling/{user_id}")
async def signaling(websocket: WebSocket, user_id: str, current_user: dict = Depends(get_current_user)):
    """
    Эндпоинт для обработки сигналов WebRTC через WebSocket.
    Подключает пользователя и передает сигналы другому пользователю.
    """
    # Проверка, что пользователь аутентифицирован (можно исключить, если в зависимости уже обрабатывается)
    if current_user.get("user_id") != user_id:
        await websocket.close()
        return

    await websocket.accept()
    active_connections[user_id] = websocket
    try:
        while True:
            # Получаем сигнал клиента
            data = await websocket.receive_text()
            signal_data = json.loads(data)

            # Передаем сигнал другому пользователю
            if 'to' in signal_data and signal_data['to'] in active_connections:
                await active_connections[signal_data['to']].send_text(json.dumps(signal_data))
            else:
                await websocket.send_text("User not connected.")
    except WebSocketDisconnect:
        # Отключаем пользователя, если соединение разорвано
        del active_connections[user_id]
        logger.info(f"User {user_id} disconnected")
