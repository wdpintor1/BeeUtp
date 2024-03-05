# forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import TB_BEE_CANALES,TB_BEE_CAMPOS
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div, Field,Fieldset
from django.forms import formset_factory

class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Agrega la clase 'form-control' a todos los widgets para mantener el estilo de Bootstrap
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''  # Oculta los textos de ayuda

        # Agrega el botón al final del formulario
        self.fields['registrar_button'] = forms.CharField(
            label='',
            widget=forms.TextInput(attrs={'type': 'submit', 'class': 'btn btn-outline-warning', 'value': 'Registrar'})
        )
            
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='', max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Correo electrónico'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'}))

class CanalForm(forms.ModelForm):
    num_campos_adicionales = 8

    class Meta:
        model = TB_BEE_CANALES
        fields = ['nombre', 'descripcion']

    def __init__(self, *args, **kwargs):
        super(CanalForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'

        campos_layout = []
        for i in range(1, self.num_campos_adicionales + 1):
            campo_name = f'campo_adicional_{i}'
            activo_name = f'activo_campo_adicional_{i}'

            self.fields[campo_name] = forms.CharField(
                required=False,
                label='',
                widget=forms.TextInput(attrs={'class': 'form-control campo-adicional', 'placeholder': f'Campo {i}'}),
            )
            self.fields[activo_name] = forms.BooleanField(required=False, label='', initial=False, widget=forms.CheckboxInput(attrs={'class': 'activo-campo'}))

            campos_layout.append(
                Div(
                    Div(
                        Field(campo_name, css_class='form-group mx-auto text-left campo-adicional-input'),
                        css_class='col-md-10 pr-6'
                    ),
                    Div(
                        Div(
                           
                            Div(
                                Field(activo_name, css_class='form-check-input mt-2 activo-campo-input'),
                                css_class='custom-checkbox'
                            ),
                            css_class='checkbox-align text-center'                            
                        ),
                        css_class='col-md-1 pr-6'
                    ),  
                    css_class='row align-items-center d-inline-flex mb-2'
                )
            )

        self.helper.layout = Layout(
            Fieldset(
                'Campos del canal:',
                *campos_layout,
                'nombre',
                'descripcion',
                Div(
                    Submit('submit', 'Guardar', css_class='btn btn-success mx-auto'),
                    css_class='text-center mt-3'                     
                ),                              
            )            
        )



class CampoForm(forms.ModelForm):
    class Meta:
        model = TB_BEE_CAMPOS
        fields = ['nombre', 'activo']
        
        def clean(self):
            cleaned_data = super().clean()
            nombre = cleaned_data.get('nombre')
            idCampo = cleaned_data.get('idCampo')

            if idCampo is not None and not nombre:
                raise forms.ValidationError('El nombre es obligatorio cuando se define un idCampo.')
        
        # Marcar campos como no requeridos        
        idCampo = forms.IntegerField(widget=forms.HiddenInput())
        nombre = forms.CharField(label='')

    def __init__(self, *args, **kwargs):
        super(CampoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'nombre',
            'activo'
        )
        # Personaliza el widget para el campo 'nombre'
        self.fields['nombre'].required = False  # Esto marca el campo como opcional
        
      
        
class CanalEditForm(forms.ModelForm):
    class Meta:
        model = TB_BEE_CANALES
        fields = ['nombre', 'descripcion']

    def __init__(self, *args, **kwargs):
        super(CanalEditForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            'nombre',
            'descripcion',
            Div(
                Submit('submit', 'Guardar', css_class='btn btn-success mx-auto'),
                css_class='text-center mt-3'
            )
        )