from django import forms


TABLE_CHOICES = [
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
    ("A11", "Table A11"),
    ("A12", "Table A12"),
    ("A13", "Table A13"),
    ("A14", "Table A14"),
    ("A15", "Table A15"),
    ("A16", "Table A16"),
    ("A17", "Table A17"),
    ("A18", "Table A18"),
    ("A19", "Table A19"),
    ("A20", "Table A20"),
]


class CheckoutForm(forms.Form):

    table_name = forms.ChoiceField(
        choices=TABLE_CHOICES,
        label="Select your table",
        widget=forms.Select(
            attrs={
                "class": "table-select",
            }
        )
    )