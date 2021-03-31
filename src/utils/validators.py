from prompt_toolkit.validation import Validator, ValidationError


class EmptyTextValidator(Validator):
    def validate(self, document):
        if len(document.text) == 0:
            raise ValidationError(message='Empty not allowed!',
                                  cursor_position=len(document.text))  # Move cursor to end


class NumberValidator(Validator):
    def validate(self, document):
        if not document.text.isdigit():
            raise ValidationError(message='Input must be a number!',
                                  cursor_position=len(document.text))