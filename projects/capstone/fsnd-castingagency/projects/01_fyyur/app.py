#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
import traceback
from flask import (
  Flask,
  render_template,
  request,
  Response,
  flash,
  redirect,
  url_for,
  abort
)
from flask_moment import Moment
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from models import *

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
# db is instantiated in models.py
db.init_app(app)
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

def flash_form_errors(form):
  for field, errors in form.errors.items():
        if not field == 'csrf_token':
          flash(form[field].label.text + ': ' + '; '.join(errors))

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')

#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  areas = []
  for loc in db.session.query(Venue.city, Venue.state).distinct().all():
    area = {}
    area['city'] = loc.city
    area['state'] = loc.state
    area['venues'] = []
    for venue in db.session.query(Venue.id, Venue.name)\
                           .filter_by(city=loc.city, state=loc.state)\
                           .order_by(Venue.name).all():
      area['venues'].append(venue)
    areas.append(area)

  return render_template('pages/venues.html', areas=areas);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  search_term = request.form.get('search_term', '').strip()
  if search_term == '':
    return redirect(url_for('venues'))

  matches = db.session.query(Venue.id, Venue.name)\
                      .filter(db.func.lower(Venue.name).contains(search_term.lower(), autoescape=True))\
                      .order_by(Venue.name).all()

  response = {
    "search_term": search_term,
    "count": len(matches),
    "data": matches
  }
  return render_template('pages/search_venues.html', results=response)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  venue = Venue.query.get_or_404(venue_id)
  venue.past_shows = []
  venue.upcoming_shows = []
  for show in venue.shows:
    show.artist_name = show.artist.name
    show.artist_image_link = show.artist.image_link
    show.start_time = str(show.start_time)
    if show.start_time < str(datetime.today()):
      venue.past_shows.append(show)
    else:
      venue.upcoming_shows.append(show)
  venue.past_shows_count = len(venue.past_shows)
  venue.upcoming_shows_count = len(venue.upcoming_shows)

  return render_template('pages/show_venue.html', venue=venue)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  return render_template('forms/new_venue.html', form=VenueForm())

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  error = False
  form = VenueForm()
  venue = Venue()

  try:
    if not form.validate():
      flash_form_errors(form)
      error = True
    elif Venue.query.filter_by(address=form.address.data, city=form.city.data, state=form.state.data).count() > 0:
      flash('Venue at this address already exists.')
      error = True
    else:
      # convert "seeking" boolean, then populate venue with form values
      form.seeking_talent.data = (form.seeking_talent.data == 'Yes')
      form.populate_obj(venue)
      db.session.add(venue)
      db.session.commit()
      db.session.refresh(venue)
      venue_id = venue.id
      # on successful db insert, flash success
      flash('Venue ' + venue.name + ' was successfully listed!')  
  except:
    db.session.rollback()
    # on unsuccessful db insert, flash an error instead
    flash('An error occurred. Venue ' + form.name.data + ' could not be listed.')
    print(traceback.format_exc())
    error = True
  finally:
    db.session.close()

  if error:
    return render_template('forms/new_venue.html', form=form)
  else:
    return redirect(url_for('show_venue', venue_id=venue_id))

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  error = False
  try:
    Venue.query.filter_by(id=venue_id).delete()
    db.session.commit()
    flash('Successfully deleted venue.')
  except:
    db.session.rollback()
    flash('An error occurred. Unable to delete venue.')
    print(traceback.format_exc())
    error = True
  finally:
    db.session.close()

  if error:
    return redirect(url_for('show_venue', venue_id=venue_id), code=303)
  else:
    return redirect(url_for('index'))

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  artists = db.session.query(Artist.id, Artist.name).order_by(Artist.name).all()
  return render_template('pages/artists.html', artists=artists)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  search_term = request.form.get('search_term', '').strip()
  if search_term == '':
    return redirect(url_for('artists'))

  matches = db.session.query(Artist.id, Artist.name)\
                      .filter(db.func.lower(Artist.name).contains(search_term.lower(), autoescape=True))\
                      .order_by(Artist.name).all()

  response = {
    "search_term": search_term,
    "count": len(matches),
    "data": matches
  }
  return render_template('pages/search_artists.html', results=response)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  artist = Artist.query.get_or_404(artist_id)
  artist.past_shows = []
  artist.upcoming_shows = []
  for show in artist.shows:
    show.venue_name = show.venue.name
    show.venue_image_link = show.venue.image_link
    show.start_time = str(show.start_time)
    if show.start_time < str(datetime.today()):
      artist.past_shows.append(show)
    else:
      artist.upcoming_shows.append(show)
  artist.past_shows_count = len(artist.past_shows)
  artist.upcoming_shows_count = len(artist.upcoming_shows)

  return render_template('pages/show_artist.html', artist=artist)

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  return render_template('forms/new_artist.html', form=ArtistForm())

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  error = False
  form = ArtistForm()
  artist = Artist()

  try:
    if not form.validate():
      flash_form_errors(form)
      error = True
    else:
      # convert "seeking" boolean, then populate artist with form values
      form.seeking_venue.data = (form.seeking_venue.data == 'Yes')
      form.populate_obj(artist)
      db.session.add(artist)
      db.session.commit()
      db.session.refresh(artist)
      artist_id = artist.id
      # on successful db insert, flash success
      flash('Artist ' + artist.name + ' was successfully listed!')
  except:
    db.session.rollback()
    # on unsuccessful db insert, flash an error instead
    flash('An error occurred. Artist ' + form.name.data + ' could not be listed.')
    print(traceback.format_exc())
    error = True
  finally:
    db.session.close()

  if error:
    return render_template('forms/new_artist.html', form=form)
  else:
    return redirect(url_for('show_artist', artist_id=artist_id))

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.get_or_404(artist_id)
  # populate form with artist values, then convert "seeking" boolean
  form.process(obj=artist)
  form.seeking_venue.data = 'Yes' if artist.seeking_venue else 'No'

  return render_template('forms/edit_artist.html', form=form, name=artist.name)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  error = False
  artist = Artist.query.get_or_404(artist_id)
  form = ArtistForm()

  try:
    if not form.validate():
      flash_form_errors(form)
      error = True
    else:
      # convert "seeking" boolean, then populate artist with form values
      form.seeking_venue.data = (form.seeking_venue.data == 'Yes')
      form.populate_obj(artist)
      db.session.commit()
  except:
    db.session.rollback()
    flash('An error occurred. Artist ' + artist.name + ' could not be updated.')
    print(traceback.format_exc())
    error = True
  finally:
    db.session.close()

  if error:
    return render_template('forms/edit_artist.html', form=form, name=artist.name)
  else:
    return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.get_or_404(venue_id)
  # populate form with venue values, then convert "seeking" boolean
  form.process(obj=venue)
  form.seeking_talent.data = 'Yes' if venue.seeking_talent else 'No'

  return render_template('forms/edit_venue.html', form=form, name=venue.name)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  error = False
  venue = Venue.query.get_or_404(venue_id)
  form = VenueForm()

  try:
    if not form.validate():
      flash_form_errors(form)
      error = True
    else:
      # convert "seeking" boolean, then populate venue with form values
      form.seeking_talent.data = (form.seeking_talent.data == 'Yes')
      form.populate_obj(venue)
      db.session.commit()
  except:
    db.session.rollback()
    flash('An error occurred. Venue ' + venue.name + ' could not be updated.')
    print(traceback.format_exc())
    error = True
  finally:
    db.session.close()

  if error:
    return render_template('forms/edit_venue.html', form=form, name=venue.name)
  else:
    return redirect(url_for('show_venue', venue_id=venue_id))

#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  shows = []
  for show in Show.query.all():
    shows.append({
        'venue_id': show.venue_id,
        'venue_name': show.venue.name,
        'artist_id': show.artist_id,
        'artist_name': show.artist.name,
        'artist_image_link': show.artist.image_link,
        'start_time': str(show.start_time)
      })

  return render_template('pages/shows.html', shows=shows)

@app.route('/shows/create', methods=['GET'])
def create_shows():
  return render_template('forms/new_show.html', form=ShowForm())

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  error = False
  form = ShowForm()
  show = Show()

  artist_id = form.artist_id.data
  venue_id = form.venue_id.data
  start_time = form.start_time.data

  try:
    if not form.validate():
      flash_form_errors(form)
      error = True
    elif Artist.query.get(artist_id) is None:
      flash('Invalid Artist ID')
      error = True
    elif Venue.query.get(venue_id) is None:
      flash('Invalid Venue ID')
      error = True
    elif Show.query.get([artist_id, venue_id, start_time]) is not None:
      flash('This show has already been listed.')
      error = True
    else:
      form.populate_obj(show)
      db.session.add(show)
      db.session.commit()
      # on successful db insert, flash success
      flash('Show was successfully listed!')
  except:
    db.session.rollback()
    # on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Show could not be listed.')
    print(traceback.format_exc())
    error = True
  finally:
    db.session.close()

  if error:
    return render_template('forms/new_show.html', form=ShowForm())
  else:
    return redirect(url_for('shows'))

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
