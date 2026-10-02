from django import forms


class CheckoutForm(forms.Form):

    table_name = forms.ChoiceField(
        label="Table Number",
        required=True,
        choices=[
            ("", "Please select your table"),
            ("A1", "Table A1"),
            ("A2", "Table A2"),
            ("A3", "Table A3"),
            ("A4", "Table A4"),
            ("A5", "Table A5"),
            ("A6", "Table A6"),
            ("A7", "Table A7"),
            ("A8", "Table A8"),
            ("A9", "Table A9"),
            ("A10", "Table A10"),
        ],
        widget=forms.Select(
            attrs={
                "class": "table-select",
                "required": True,
            }
        )
    )