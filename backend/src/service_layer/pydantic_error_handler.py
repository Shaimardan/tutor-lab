from pydantic import ValidationError
from pydantic_core import ErrorDetails


class PydanticErrorHandler:
    DEFAULT_CUSTOM_MESSAGE_RU = "Ошибка валидации"
    CUSTOM_MESSAGES_RU = {
        "missing": "Поле обязательно для заполнения",
        "int_parsing": "Значение должно быть целым числом",
        "url_scheme": "Эй, используйте правильную схему URL! Требовались схемы: {expected_schemes}",
        "greater_than_equal": "Значение должно быть больше или равно {ge}",
        "greater_than": "Значение должно быть больше {gt}",
        "less_than_equal": "Значение должно быть меньше или равно {le}",
        "less_than": "Значение должно быть меньше {le}",
    }

    @staticmethod
    def convert_errors(
        e: ValidationError, custom_message_dict: dict[str, str] | None = None
    ) -> list[ErrorDetails]:
        """Изменяет сообщение сообщение ошибки на кастомнные.

        Args:
            e: Ошибка валидации Pydantic
            custom_message_dict: Список кастомных сообщений.
            Всевозможные ключи ошибок валидации можно проверить по ссылке:
                https://docs.pydantic.dev/latest/errors/validation_errors/

        Returns:
            Список ошибок с кастомным сообщением об ошибки
        """
        if custom_message_dict is None:
            custom_message_dict = PydanticErrorHandler.CUSTOM_MESSAGES_RU
        new_errors: list[ErrorDetails] = []
        for error in e.errors():
            custom_message = custom_message_dict.get(
                error["type"], PydanticErrorHandler.DEFAULT_CUSTOM_MESSAGE_RU
            )
            if custom_message:
                ctx = error.get("ctx")
                error["msg"] = custom_message.format(**ctx) if ctx else custom_message
            new_errors.append(error)
        return new_errors

    @staticmethod
    def get_msg_from_error(e: list[ErrorDetails]) -> list[dict[str, str]]:
        parsed_errors = []
        for error in e:
            field = error.get("loc", [""])[0]
            msg = error.get("msg", "")
            dict_info = {"key": field, "message": msg}
            if dict_info not in parsed_errors:
                parsed_errors.append(dict_info)
        return parsed_errors
