from typing import Optional, Any, List
from fastapi import HTTPException, status

from db.repositories.job_repositories.job_application_repository import JobApplicationRepository
from db.schemas.job_schemas.job_application_schemas import JobApplicationCreateSchema, JobApplicationResponseSchema
from db.repositories.master_repositories.master_repositories import MasterRepository
from db.repositories.salon_repositories.salon_repositories import SalonRepository
from use_case.utils.permissions import UserAccessService
from config.components.logging_config import logger


class JobApplicationService:
    @staticmethod
    async def create_job_application(
            data: JobApplicationCreateSchema,
            current_user: dict,
    ) -> JobApplicationResponseSchema:
        
        try:
            user_id = current_user.get("user_id")
            user_role = current_user.get("role")

            # Получаем master_id
            master_id = await UserAccessService.get_master_or_salon_id(
                user_role=user_role,
                user_id=user_id,
                master_repository=MasterRepository,
                salon_repository=SalonRepository
            )

            if not master_id:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Мастер не найден"
                )

            # Создаем словарь с данными
            data_dict = data.dict()
            data_dict["master_id"] = master_id

            logger.info(f"Создание заявки с данными: {data_dict}")
            # Создаем заявку через репозиторий
            job_application = await JobApplicationRepository.create_job_application(**data_dict)

            # Возвращаем объект через распаковку __dict__
            return JobApplicationResponseSchema(**job_application.__dict__)
        except HTTPException as http_ex:
            # Пробрасываем HTTP исключения дальше
            raise http_ex
        except Exception as e:
            logger.error(f"Ошибка при создании заявки: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Ошибка при создании заявки: {str(e)}"
            )