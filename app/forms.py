from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional


class RegisterForm(FlaskForm):

    full_name = StringField(
        "Full Name",
        validators=[DataRequired(), Length(min=3)]
    )

    email = StringField(
        "Email",
        validators=[DataRequired(), Email()]
    )

    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(min=6)]
    )

    confirm_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), EqualTo("password", message="Passwords must match.")]
    )

    submit = SubmitField("Create Account")


class LoginForm(FlaskForm):

    email = StringField(
        "Email",
        validators=[DataRequired(), Email()]
    )

    password = PasswordField(
        "Password",
        validators=[DataRequired()]
    )

    submit = SubmitField("Login")


class SymptomLogForm(FlaskForm):

    severity = SelectField(
        "How are you feeling today?",
        choices=[
            ("1", "1 - Mild"),
            ("2", "2 - Noticeable"),
            ("3", "3 - Moderate"),
            ("4", "4 - Severe"),
            ("5", "5 - Emergency-level"),
        ],
        validators=[DataRequired()],
    )

    symptoms = StringField(
        "Symptoms (e.g. wheezing, itchy eyes, cough)",
        validators=[Optional(), Length(max=200)]
    )

    notes = StringField(
        "Notes — what were you doing or exposed to?",
        validators=[Optional(), Length(max=300)]
    )

    submit = SubmitField("Log entry")


class TravelCheckForm(FlaskForm):

    destination = StringField(
        "Destination or event location",
        validators=[DataRequired(), Length(max=150)]
    )

    air_quality_level = SelectField(
        "Expected air quality",
        choices=[
            ("Low", "Low pollution"),
            ("Moderate", "Moderate pollution"),
            ("High", "High pollution / smoky"),
        ],
        validators=[DataRequired()],
    )

    pollen_level = SelectField(
        "Expected pollen level",
        choices=[
            ("None", "Low / none"),
            ("Moderate", "Moderate"),
            ("High", "High"),
        ],
        validators=[DataRequired()],
    )

    submit = SubmitField("Check risk")


class HealthProfileForm(FlaskForm):

    disease = StringField(
        "Condition (e.g. Asthma, COPD, Pollen Allergy)",
        validators=[Optional(), Length(max=100)]
    )

    medication = StringField(
        "Current Medication",
        validators=[Optional(), Length(max=100)]
    )

    trigger = StringField(
        "Known Triggers (e.g. dust, pollen, high humidity)",
        validators=[Optional(), Length(max=150)]
    )

    submit = SubmitField("Save Profile")
