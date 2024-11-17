from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, InputRequired, Regexp
from app_barbea_01.models import Usuario
from flask_login import current_user

class FormCriarConta(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    confirmacao_senha = PasswordField('Confirmação da Senha', validators=[DataRequired(), EqualTo('senha')])
    botao_submit_criarconta = SubmitField('Criar Conta')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('Email já cadastrado. Faça login para continuar.')

class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    lembrar_dados = BooleanField('Lembrar Dados de Acesso')
    botao_submit_login = SubmitField('Fazer Login')

class Form_Agendar(FlaskForm):
    lista_horas = [8, 9, 10, 11, 12, 14, 15, 16]

    horarios_disponiveis = [(str(hora) + ':00', str(hora) + ':00') for hora in lista_horas]

    username = StringField('Nome', validators=[DataRequired()])
    cell = StringField("() + Celular", validators=[DataRequired(), Length(11, 11)])
    servico = SelectField('Serviço',
                          choices=[('Corte de Cabelo', 'Corte de Cabelo'), ('Corte de Barba', 'Corte de Barba'),
                                   ('Corte de Cabelo e Barba', 'Corte de Cabelo e Barba')], validators=[DataRequired()])
    datar = DateField('Data', format='%d/%m/%Y', validators=[DataRequired()],
                      render_kw={"data-do-not-use-csrf": "true"})
    hora = SelectField('Hora', choices=horarios_disponiveis, validators=[DataRequired()])
    botao_submit_agendar = SubmitField('Agendar')


class Form_EditarPerfil(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    foto_perfil = FileField('Atualizar Foto', validators=[FileAllowed(['jpg', 'png'])])
    botao_submit_editarperfil = SubmitField('Confirmar Edição')

    # verifica se ja existe o email no bd, se sim exibe um erro no form
    def validate_email(self, email):
        if current_user.email != email.data:
            usuario = Usuario.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError('Já existe um usuário com esse e-mail. Cadastre outro e-mail ou faça Login')