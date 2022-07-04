from datetime import datetime
from typing import Dict, List
from django.db.models import QuerySet, Max
from rest_framework import generics, exceptions, response
from handbooks.models import Handbook, HandbookElement
from handbooks.serializers import HandbookSerializer, HandbookElementSerializer
from handbooks.pagination import ResultsSetPagination


class HandbookList(generics.ListAPIView):
    """Представление для вывода справочников актуальных по дате
    """
    serializer_class = HandbookSerializer
    pagination_class = ResultsSetPagination

    def get_queryset(self):
        # Проверяем, есть ли дата в параметрах,
        # в противном случае возвращаем полный список справочников
        if 'date' not in self.kwargs:
            return Handbook.objects.all()

        # Проверяем дату на валидность, в противном случае возвращаем ошибку
        try:
            cleaned_date: datetime = \
                datetime.strptime(self.kwargs['date'], '%Y-%m-%d')
        except ValueError:
            raise exceptions.ParseError('Некорректная дата')
        # Выбираем справочники по дате, соответствующей запросу и
        # возвращаем список (id справочника, дата) в формате строки
        actual_handbooks: List[str] = [
            '(%d, \'%s\')' % (
                handbook['handbook_id'],
                handbook['max_date'].strftime('%Y-%m-%d')
            )
            for handbook
            in list(
                Handbook.objects.filter(start_at__lte=cleaned_date)
                                .values('handbook_id')
                                .annotate(max_date=Max('start_at'))
            )
        ]
        # Формируем строку фильтрации запроса по актуальным справочникам
        where_statement: str = '(handbook_id, start_at) in ({})'.format(
            ','.join(actual_handbooks)
        )
        # Запрос
        queryset = Handbook.objects.extra(
            where=[where_statement],
        ).order_by()
        return queryset


class ElementsList(generics.ListAPIView):
    """Предсталение для вывода элементов актуального справочника
    """
    serializer_class = HandbookElementSerializer
    pagination_class = ResultsSetPagination

    @staticmethod
    def _validate_element(query_params: Dict[str, str],
                          queryset: QuerySet[HandbookElement]) -> bool:
        """Метод для валидации элементов

        :param query_params: Параметры адресной строки
        :type query_params: Dict[str, str]
        :param queryset: Выборка соответствующая списку элементов справочника
        :type queryset: QuerySet[HandbookElement]
        :raises exceptions.ParseError: Ошибка при некорректном количестве
                                        валидируемых параметров
        :return: Валидный параметр или нет
        :rtype: bool
        """
        element_code: str = query_params.get('code')
        element_value: str = query_params.get('value')
        if len(element_code) != 1 or len(element_value) != 1:
            raise exceptions.ParseError(
                'Параметр для валидации должен быть один'
            )
        return (
            (element_code[0], element_value[0]) in
            list(queryset.values_list('element_code', 'value'))
        )

    def get(self, request, *args, **kwargs):
        # Если в query string есть параметры, то валидируем
        if len(request.query_params) > 0:
            if self._validate_element(dict(request.query_params),
                                      self.get_queryset()):
                return response.Response({'validate': True})
            else:
                return response.Response({'validate': False})
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        # Формируем фильтр справочников
        # по идентификатору справочника
        handbooks: QuerySet[Handbook] = \
            Handbook.objects.filter(handbook_id=self.kwargs['handbook'])
        if not handbooks:
            raise exceptions.ParseError(
                'Некорректный идентификатор справочника'
            )
        # по дате начала действия
        if 'version' in self.kwargs:
            try:
                start_at = Handbook.objects.get(
                    handbook_id=self.kwargs['handbook'],
                    version=self.kwargs['version']
                ).start_at
            except Handbook.DoesNotExist:
                raise exceptions.ParseError(
                    'Некорректный номер версии справочника'
                )
            except Handbook.MultipleObjectsReturned:
                raise exceptions.ParseError(
                    'Дубликат версии справочника'
                )
            handbooks: QuerySet[Handbook] = \
                Handbook.objects.filter(start_at__lte=start_at)
        # Выбираем актуальные коды и даты соответтвующих параметрам элементов
        actual_code_dates: List[str] = [
            (
                element['element_code'],
                element['max_date']
            )
            for element
            in list(
                HandbookElement.objects.select_related('handbook_id')
                                       .filter(handbook_id__in=handbooks)
                                       .values('element_code')
                                       .annotate(
                                        max_date=Max('handbook_id__start_at')
                                       )
            )
        ]
        # Выбираем среди элементов соответствующие параметрам запроса
        actual_ids: List[int] = []
        for element in HandbookElement.objects.select_related('handbook_id')\
                                              .filter(
                                                handbook_id__in=handbooks
                                              ):
            if (
                element.element_code, element.handbook_id.start_at
            ) in actual_code_dates:
                actual_ids.append(element.id)
        # Финальный запрос
        queryset: QuerySet[HandbookElement] = \
            HandbookElement.objects.filter(id__in=actual_ids)
        return queryset
