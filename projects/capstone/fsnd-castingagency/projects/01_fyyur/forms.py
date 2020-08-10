from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, TextAreaField
from wtforms.validators import InputRequired, Optional, URL, Regexp, ValidationError

STATE_CHOICES = [
    ('AL', 'AL'),
    ('AK', 'AK'),
    ('AZ', 'AZ'),
    ('AR', 'AR'),
    ('CA', 'CA'),
    ('CO', 'CO'),
    ('CT', 'CT'),
    ('DE', 'DE'),
    ('DC', 'DC'),
    ('FL', 'FL'),
    ('GA', 'GA'),
    ('HI', 'HI'),
    ('ID', 'ID'),
    ('IL', 'IL'),
    ('IN', 'IN'),
    ('IA', 'IA'),
    ('KS', 'KS'),
    ('KY', 'KY'),
    ('LA', 'LA'),
    ('ME', 'ME'),
    ('MT', 'MT'),
    ('NE', 'NE'),
    ('NV', 'NV'),
    ('NH', 'NH'),
    ('NJ', 'NJ'),
    ('NM', 'NM'),
    ('NY', 'NY'),
    ('NC', 'NC'),
    ('ND', 'ND'),
    ('OH', 'OH'),
    ('OK', 'OK'),
    ('OR', 'OR'),
    ('MD', 'MD'),
    ('MA', 'MA'),
    ('MI', 'MI'),
    ('MN', 'MN'),
    ('MS', 'MS'),
    ('MO', 'MO'),
    ('PA', 'PA'),
    ('RI', 'RI'),
    ('SC', 'SC'),
    ('SD', 'SD'),
    ('TN', 'TN'),
    ('TX', 'TX'),
    ('UT', 'UT'),
    ('VT', 'VT'),
    ('VA', 'VA'),
    ('WA', 'WA'),
    ('WV', 'WV'),
    ('WI', 'WI'),
    ('WY', 'WY'),
]

GENRE_CHOICES = [
    ('Alternative', 'Alternative'),
    ('Blues', 'Blues'),
    ('Classical', 'Classical'),
    ('Country', 'Country'),
    ('Electronic', 'Electronic'),
    ('Folk', 'Folk'),
    ('Funk', 'Funk'),
    ('Hip-Hop', 'Hip-Hop'),
    ('Heavy Metal', 'Heavy Metal'),
    ('Instrumental', 'Instrumental'),
    ('Jazz', 'Jazz'),
    ('Musical Theatre', 'Musical Theatre'),
    ('Pop', 'Pop'),
    ('Punk', 'Punk'),
    ('R&B', 'R&B'),
    ('Reggae', 'Reggae'),
    ('Rock n Roll', 'Rock n Roll'),
    ('Soul', 'Soul'),
    ('Other', 'Other'),
]

SEEKING_CHOICES = [('Yes', 'Yes'), ('No', 'No')]

PHONE_REGEX = '^\d?-?\d{3}-?\d{3}-?\d{4}$'

class ShowForm(FlaskForm):
    artist_id = StringField(
        'Artist ID', validators=[InputRequired()]
    )
    venue_id = StringField(
        'Venue ID', validators=[InputRequired()]
    )
    start_time = DateTimeField(
        'Start Time',
        validators=[InputRequired()],
        default=datetime.today()
    )

class VenueForm(FlaskForm):
    name = StringField(
        'Name', validators=[InputRequired()]
    )
    address = StringField(
        'Address', validators=[InputRequired()]
    )
    city = StringField(
        'City', validators=[InputRequired()]
    )
    state = SelectField(
        'State', validators=[InputRequired()],
        choices=STATE_CHOICES
    )
    phone = StringField(
        'Phone', validators=[Regexp(PHONE_REGEX), Optional()]
    )
    website = StringField(
        'Website', validators=[URL(), Optional()]
    )
    facebook_link = StringField(
        'Facebook Link', validators=[URL(), Optional()]
    )
    image_link = StringField(
        'Image Link', validators=[URL(), Optional()]
    )
    genres = SelectMultipleField(
        'Genres', validators=[InputRequired()],
        choices=GENRE_CHOICES
    )
    seeking_talent = SelectField(
        'Seeking Talent?', choices=SEEKING_CHOICES
    )
    seeking_description = TextAreaField(
        'Description'
    )

class ArtistForm(FlaskForm):
    name = StringField(
        'Name', validators=[InputRequired()]
    )
    city = StringField(
        'City', validators=[InputRequired()]
    )
    state = SelectField(
        'State', validators=[InputRequired()],
        choices=STATE_CHOICES
    )
    phone = StringField(
        'Phone', validators=[Regexp(PHONE_REGEX), Optional()]
    )
    website = StringField(
        'Website', validators=[URL(), Optional()]
    )
    facebook_link = StringField(
        'Facebook Link', validators=[URL(), Optional()]
    )
    image_link = StringField(
        'Image Link', validators=[URL(), Optional()]
    )
    genres = SelectMultipleField(
        'Genres', validators=[InputRequired()],
        choices=GENRE_CHOICES
    )
    seeking_venue = SelectField(
        'Seeking Venues?', choices=SEEKING_CHOICES
    )
    seeking_description = TextAreaField(
        'Description'
    )
