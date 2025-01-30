from typing import Optional, Any, List
from fastapi import HTTPException, status

from db.repositories.job_repositories.vacancy_salon_repository import VacancyRepository
from db.repositories.master_repositories.master_repositories import MasterRepository
from db.repositories.salon_repositories.salon_repositories import SalonRepository
from db.schemas.job_schemas.vacancy_salon_schemas import VacancyCreateSchema, VacancyResponseSchema
from db.repositories.salon_repositories.salon_master_relation_repositoies import SalonMasterRelationRepository
from use_case.utils.permissions import UserAccessService
from config.components.logging_config import logger


class VacancyService:
    @staticmethod
    async def create_vacancy_salon(
            data: VacancyCreateSchema,
            current_user: dict,
    ) -> VacancyResponseSchema:
        try:
            user_id = current_user.get("user_id")
            user_role = current_user.get("role")

            if not user_id or not user_role:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Отсутствуют данные пользователя"
                )

            # Получаем master_id или salon_id
            salon_id = await UserAccessService.get_master_or_salon_id(
                user_role=user_role,
                user_id=user_id,
                master_repository=MasterRepository,
                salon_repository=SalonRepository
            )

            if not salon_id:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Салон не найден"
                )

            # Создаем словарь с данными
            vacancy_data = data.dict()
            vacancy_data["salon_id"] = salon_id

            # Создаем вакансию
            vacancy = await VacancyRepository.create_vacancy(**vacancy_data)

            if not vacancy:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Не удалось создать вакансию"
                )

            return VacancyResponseSchema(**vacancy.__dict__)

        except HTTPException as http_ex:
            raise http_ex
        except Exception as e:
            logger.error(f"Ошибка в сервисе создания вакансии: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Ошибка при создании вакансии: {str(e)}"
            )

    @staticmethod
    async def delete_vacancy_salon(
            vacancy_id: int,
            current_user: dict,
) -> bool:
        user_id = current_user.get("user_id")
        user_role = current_user.get("role")

        # Получаем master_id или salon_id
        salon_id = await UserAccessService.get_master_or_salon_id(
            user_role=user_role,
            user_id=user_id,
            master_repository=MasterRepository,
            salon_repository=SalonRepository
        )

        # Получаем id салона связаный с вакансией
        salon_id_vacancy = await VacancyRepository.get_salon_by_vacancy_id(vacancy_id)

        if salon_id_vacancy != salon_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Вы не можете удалять вакансию, так как вы не создавали ее"
            )
        await VacancyRepository.delete_vacancy(vacancy_id)
        return True

