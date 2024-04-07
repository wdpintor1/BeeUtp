from django import forms
from manage.models import TB_BEE_GRAFICA, TB_BEE_CAMPOS
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div

class GraficaForm(forms.ModelForm):
    class Meta:
        model = TB_BEE_GRAFICA
        fields = ['titulo', 'ejeX', 'ejeY', 'color', 'backGround', 'Tipo', 'Datos', 'idCampo']
        labels = {
            'titulo': 'Título',
            'ejeX': 'Eje X',
            'ejeY': 'Eje Y',
            'color': 'Color',
            'backGround': '',
            'Tipo': 'Tipo',
            'Datos': '# Datos',
            'idCampo': '',
        }

    def __init__(self, id_canal, *args, **kwargs):
        super(GraficaForm, self).__init__(*args, **kwargs)
        
        # Personaliza widgets si es necesario, por ejemplo, para el color y el campo
        self.fields['color'].widget = forms.TextInput(attrs={'type': 'color'})
        self.fields['Datos'].widget = forms.NumberInput(attrs={'type': 'number'})
        #self.fields['backGround'].widget = forms.TextInput(attrs={'type': 'color'})

        self.fields['idCampo'].required = False
        self.fields['idCampo'].widget.attrs['hidden'] = True
         # Establece el valor predeterminado y deshabilita el campo Tipo
        self.fields['Tipo'].initial = 'lineal'
        self.fields['Tipo'].widget.attrs['disabled'] = True
        # Añade clases a los campos de color
        self.fields['color'].widget.attrs['class'] = 'color-selector'
        #self.fields['backGround'].widget.attrs['class'] = 'color-selector'
        self.fields['backGround'].widget.attrs['hidden'] = True
        
        # Configuración de crispy-forms para agregar un botón de submit
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'titulo', 'ejeX', 'ejeY', 'color', 'backGround', 'Tipo', 'Datos', 'idCampo',
            Div(
                Submit('submit', 'Guardar', css_class='btn btn-success mx-auto'),
                css_class='text-center mt-3'
            )
        )
