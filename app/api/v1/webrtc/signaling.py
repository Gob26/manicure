from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
import json

from use_case.utils.jwt_handler import get_current_user
from config.components.logging_config import logger

active_connections = {}

signal_router = APIRouter()


@signal_router.websocket("/{user_id}")
async def signaling(websocket: WebSocket, user_id: str, current_user: dict = Depends(get_current_user)):
    """
    Эндпоинт для обработки сигналов WebRTC через WebSocket.
    Подключает пользователя и передает сигналы другому пользователю.
    """
    # Проверка, что пользователь аутентифицирован
    if current_user.get("user_id") != user_id:
        await websocket.close()
        return

    await websocket.accept()
    active_connections[user_id] = websocket
    logger.info(f"Пользователь {user_id} подключился")

    try:
        while True:
            # Получаем сигнал клиента
            data = await websocket.receive_text()
            signal_data = json.loads(data)

            signal_type = signal_data.get("type")
            target_id = signal_data.get("to")

            logger.info(f"Получен {signal_type} от {user_id} для {target_id}")

            # Проверяем, подключен ли адресат
            if target_id in active_connections:
                try:
                    await active_connections[target_id].send_text(json.dumps(signal_data))
                    logger.info(f"Отправлен {signal_type} от {user_id} в {target_id}")
                except Exception as e:
                    logger.error(f"Ошибка при отправке {signal_type} от {user_id} в {target_id}: {str(e)}")
            else:
                try:
                    await websocket.send_text(json.dumps({"error": "Пользователь не подключен"}))
                except Exception as e:
                    logger.error(f"Ошибка при отправке ошибки пользователю {user_id}: {str(e)}")

    except WebSocketDisconnect:
        del active_connections[user_id]
        logger.info(f"Пользователь {user_id} отключен")
