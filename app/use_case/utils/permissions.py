# utils/permissions.py
from fastapi import HTTPException, status

from config.components.logging_config import logger


def check_user_permission(current_user: dict, allowed_roles: list):
    """
    Проверяет, есть ли у текущего пользователя права доступа.

    :param current_user: Данные текущего пользователя
    :param allowed_roles: Список ролей, которые могут выполнить действие
    :raises HTTPException: Если у пользователя нет нужных прав
    """
    if current_user["role"] not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="У вас нет прав для выполнения этого действия"
        )


class UserAccessService:
    @staticmethod
    async def get_master_or_salon_id(
            user_role: str,
            user_id: int,
            master_repository,
            salon_repository
    ) -> int:
        """
        Получает master_id или salon_id на основании роли пользователя.

        :param user_role: Роль пользователя (например, "master" или "salon").
        :param user_id: ID пользователя.
        :param master_repository: Репозиторий мастеров.
        :param salon_repository: Репозиторий салонов.
        :return: ID мастера или салона.
        :raises HTTPException: Если данные не найдены или роль не разрешена.
        """
        logger.info(f"Роль пользователя: {user_role}. Получаем связанную информацию.")

        if user_role == "master":
            master = await master_repository.get_master_by_user_id(user_id=user_id)
            if master:
                logger.info(f"Мастер найден с ID {master.id}")
                return master.id
            else:
                logger.error(f"Мастер с user_id {user_id} не найден")
                raise HTTPException(status_code=404, detail="Мастер не найден")

        elif user_role == "salon":
            salon = await salon_repository.get_salon_by_user_id(user_id=user_id)
            if salon:
                logger.info(f"Салон найден с ID {salon.id}")
                return salon.id
            else:
                logger.error(f"Салон с user_id {user_id} не найден")
                raise HTTPException(status_code=404, detail="Салон не найден")

        else:
            logger.error(f"Роль пользователя {user_role} не разрешена")
            raise HTTPException(status_code=403, detail="Роль пользователя не разрешена")

    @staticmethod
    async def check_admin_or_owner_permission(
            user_role: str,
            user_id: int | str,
            custom_service,
            master_repository,
            salon_repository
    ):
        logger.info(f"Начало проверки прав")
        logger.info(f"Входные параметры: user_role={user_role}, user_id={user_id}")

        user_id = int(user_id) if isinstance(user_id, str) else user_id

        if user_role == "admin":
            logger.info("Пользователь - администратор, доступ разрешен")
            return

        try:
            # Получаем ID мастера или салона
            user_entity_id = await UserAccessService.get_master_or_salon_id(
                user_role=user_role,
                user_id=user_id,
                master_repository=master_repository,
                salon_repository=salon_repository,
            )
            logger.info(f"Получен user_entity_id: {user_entity_id}")

            # Проверяем права для мастера
            if user_role == "master":
                logger.info(
                    f"Проверка прав мастера: master_id услуги={custom_service.master_id}, user_entity_id={user_entity_id}")
                if custom_service.master_id != user_entity_id:
                    logger.warning(f"Отказ в доступе: master_id {custom_service.master_id} не совпадают")
                    raise HTTPException(status_code=403, detail="Нет прав для выполнения операции")

            # Проверяем права для салона
            elif user_role == "salon":
                logger.info(
                    f"Проверка прав салона: salon_id услуги={custom_service.salon_id}, user_entity_id={user_entity_id}")
                if custom_service.salon_id != user_entity_id:
                    logger.warning("Отказ в доступе: salon_id не совпадают")
                    raise HTTPException(status_code=403, detail="Нет прав для выполнения операции")

            logger.info("Проверка прав успешно завершена")

        except Exception as e:
            logger.error(f"Ошибка при проверке прав: {str(e)}", exc_info=True)
            raise


    @staticmethod
    def check_user_permission(current_user: dict, allowed_roles: list):
        """
        Проверяет, есть ли у текущего пользователя права доступа.
        ПРИМЕР:
        UserAccessService.check_user_permission(current_user, ["master", "admin"])
        :param current_user: Данные текущего пользователя.
        :param allowed_roles: Список ролей, которые могут выполнить действие.
        :raises HTTPException: Если у пользователя нет нужных прав.
        """
        logger.info(f"Проверка прав пользователя с ролью {current_user['role']}. Разрешённые роли: {allowed_roles}")

        if current_user["role"] not in allowed_roles:
            logger.error("У пользователя нет прав для выполнения действия.")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="У вас нет прав для выполнения этого действия"
            )

        logger.info("Права пользователя подтверждены.")
