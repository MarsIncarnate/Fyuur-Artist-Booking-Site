from __future__ import absolute_import
from dataclasses import dataclass
from distutils.log import info
from email import message
import json
from sys import unraisablehook
from typing import final
from unicodedata import name
from unittest import result
from click import echo
import dateutil.parser
import babel
from flask import render_template, request, Response, flash, redirect, url_for, abort, jsonify
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from sqlalchemy import false
from forms import *
from datetime import datetime
import os
from flask_moment import Moment
from models import Show, Venue, Artist, app, db

moment = Moment(app)

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime


@app.route('/')
def index():
  # recent_artists=Artist.query.order_by(db.desc(Artist.created_date)).limit(10).all() 
  # recent_venues=Venue.query.order_by(db.desc(Venue.created_date)).limit(10).all()
  return render_template('pages/home.html')

#venues

@app.route('/venues')
def venues():
  data = []
  places = Venue.query.all()
  cities = set([v.city for v in places])
    
  for city in cities: 
    same_city_venue = Venue.query.filter_by(city=city).order_by('name').all()
    data.append({
      "city": same_city_venue[0].city,
      "state": same_city_venue[0].state,
      "venues": [{
        'id':same_city.id, 
        'name':same_city.name, 
        'num_upcoming_shows':Show.query.filter_by(venue_id=same_city.id).count()} 
          for same_city in same_city_venue]
        })
      
   
    return render_template('pages/venues.html', areas=data)

  # try:
  #   places = Venue.query.distinct(Venue.city, Venue.state).all()
  #   data = []
  #   for venue in places:
  
# def venue_search_result(search_term):
#    try:
#      data = Venue.query.filter(db.func.lower(Venue.name).like(f"%{search_term.lower()}%")).order_by('name').all()
#      return data
  
#    except Exception as e:
#      print(e)

# venues search

@app.route('/venues/search', methods=['POST'])
def search_venues():
  try:
    search_term = request.form.get("search_term", "")

    response = {}
    venues = list(Venue.query.filter(
          Venue.name.ilike(f"%{search_term}%") |
          Venue.state.ilike(f"%{search_term}%") |
          Venue.city.ilike(f"%{search_term}%") 
      ).all())
    response["count"] = len(venues)
    response["data"] = []

    for venue in venues:
      venue_unit = {
              "id": venue.id,
              "name": venue.name,
              "num_upcoming_shows": len(list(filter(lambda x: x.start_time > datetime.now(), venue.artists_show)))
          }
      response["data"].append(venue_unit)

    return render_template('pages/search_venues.html', results=response, search_term=search_term)

  except:
     flash('we are unable to fetch your search results at this moment')
     return redirect(url_for('index'))
  
#show venue

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  no_show = False
        
  venue_details=Venue.query.filter_by(id=venue_id).join(Show, Show.venue_id==Venue.id).join(Artist, Artist.id==Show.artist_id).add_columns(Artist.id, Artist.name, Artist.image_link, Show.start_time).all()
       
  past_shows =[]
  upcoming_shows=[]
        
  if venue_details:
    for detail in venue_details:
      if detail.start_time < datetime.today():
        past_shows.append({
          "venue_id": detail.id,
          "venue_name": detail.name,
          "venue_image_link": detail.image_link,
          "start_time": f'{detail.start_time}'
          })
      else:
        upcoming_shows.append({
          "venue_id": detail.id,
          "venue_name": detail.name,
          "venue_image_link": detail.image_link,
          "start_time": f'{detail.start_time}'
          })
  else:
    venue_details = Venue.query.filter_by(id=venue_id).all()
    no_show = True
            
  for detail in venue_details:
    venue_info={
    'id': detail.Venue.id if not no_show else detail.id,
    'name':detail.Venue.name if not no_show else detail.name,
    'genres':detail.Venue.genres if not no_show else detail.genres,
    'city': detail.Venue.city if not no_show else detail.city,
    'state': detail.Venue.state if not no_show else detail.state,
    'phone': detail.Venue.phone if not no_show else detail.phone,
    'website': detail.Venue.website if not no_show else detail.website,
    'facebook_link': detail.Venue.facebook_link if not no_show else detail.facebook_link,
    'seeking_venue': detail.Venue.seeking_talent == 'y' if not no_show else detail.seeking_talent == 'y',
    'seeking_description': detail.Venue.seeking_description if not no_show else detail.seeking_description,
    'image_link': detail.Venue.image_link if not no_show else detail.image_link,
    'past_shows': past_shows,
    'upcoming_shows':upcoming_shows,
    'past_shows_count':len(past_shows),
    'upcoming_shows_count':len(upcoming_shows)
    }

  return render_template('pages/show_artist.html', artist=venue_info)

  
 #edit venues

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = Venue.query.get(venue_id)
    form.genres.data = venue.genres

    return render_template('forms/edit_venue.html', form=form, venue=venue)
  
@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  form = VenueForm(request.form)
  if form.validate():
    try:
      venue = Venue.query.get(venue_id)

      venue.name = form.name.data
      venue.city=form.city.data
      venue.state=form.state.data
      venue.address=form.address.data
      venue.phone=form.phone.data
      venue.genres=",".join(form.genres.data)
      venue.facebook_link=form.facebook_link.data
      venue.image_link=form.image_link.data
      venue.seeking_talent=form.seeking_talent.data
      venue.seeking_description=form.seeking_description.data
      venue.website=form.website_link.data

      db.session.add(venue)
      db.session.commit()

      flash("Venue " + form.name.data + " edited successfully")
      return redirect(url_for('show_venue', venue_id=venue_id))

    except:
     flash('venue could not be edited successfully')
     return redirect(url_for('index'))

    finally:
      db.session.close()

  else:
    flash('please submit valid form results')
    return redirect(url_for('index'))


#venues creation

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  form = VenueForm(request.form)
  if form.validate():
    try:
      venue = Venue(name=request.form['name'], city=request.form['city'], state=request.form['state'], address=request.form['address'], phone=request.form['phone'], image_link=request.form['image_link'], genres=request.form.getlist('genres', type=str), facebook_link=request.form['facebook_link'], website=request.form['website_link'], seeking_talent="seeking_talent" in request.form, seeking_description=request.form['seeking_description'])
      db.session.add(venue)
      db.session.commit()  
      flash('venue ' + request.form['name'] + ' was successfully listed!')
    except:
      flash('Venue' + (request.form['name']) + 'could not be listed at this moment')
      db.session.rollback()
    finally:
      db.session.close()
      return redirect(url_for('index'))

#delete 
@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  try:
    Venue.query.filter_by(Venue.id == venue_id).delete()
    db.session.commit()
  except:
    flash(f'venue (venue_id)could not be deleted at this moment', category="error")
    db.session.rollback()
    abort(500)
  finally:
    db.session.close()
    return jsonify({ 'success': True })

#artists

@app.route('/artists')
def artists():
  data =[]
  artists = Artist.query.order_by('name').all()
  for artist in artists:
    data.append({
        "id": artist.id,
        "name": artist.name,
      })
  return render_template('pages/artists.html', artists=data)

       
#artists search

@app.route('/artists/search', methods=['POST'])
def search_artists():
  search_term=request.form.get('search_term', '')
  try:
    search_results=Artist.query.filter (Artist.name.ilike('%'+search_term+'%')).order_by('id').all()
    if len(search_results)==0:
      flash(f'Your search: "{search_term}" has no matching records.')
    response={"count": len(search_results), "data": [{"id":search_result.id, "name":search_result.name, "num_of_upcoming_shows": Show.query.filter_by(venue_id=search_result.id).count()} for search_result in search_results]
          }
  except:
     flash('we are unable to fetch your search results at this moment')
     return redirect(url_for('index'))

  return render_template('pages/search_artists.html', results=response, search_term=search_term)

#show artists

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):

  no_show = False
        
  artist_details=Artist.query.filter_by(id=artist_id).join(Show, Show.artist_id==Artist.id).join(Venue, Venue.id==Show.venue_id).add_columns(Venue.id, Venue.name, Venue.image_link, Show.start_time).all()
       
  past_shows =[]
  upcoming_shows=[]
        
  if artist_details:
    for detail in artist_details:
      if detail.start_time < datetime.today():
        past_shows.append({
          "artist_id": detail.id,
          "artist_name": detail.name,
          "artist_image_link": detail.image_link,
          "start_time": f'{detail.start_time}'
          })
      else:
        upcoming_shows.append({
          "artist_id": detail.id,
          "artist_name": detail.name,
          "artist_image_link": detail.image_link,
          "start_time": f'{detail.start_time}'
          })
  else:
    artist_details = Artist.query.filter_by(id=artist_id).all()
    no_show = True
            
  for detail in artist_details:
    artist_info={
    'id': detail.Artist.id if not no_show else detail.id,
    'name':detail.Artist.name if not no_show else detail.name,
    'genres':detail.Artist.genres if not no_show else detail.genres,
    'city': detail.Artist.city if not no_show else detail.city,
    'state': detail.Artist.state if not no_show else detail.state,
    'phone': detail.Artist.phone if not no_show else detail.phone,
    'website': detail.Artist.website if not no_show else detail.website,
    'facebook_link': detail.Artist.facebook_link if not no_show else detail.facebook_link,
    'seeking_venue': detail.Artist.seeking_venue == 'y' if not no_show else detail.seeking_venue == 'y',
    'seeking_description': detail.Artist.seeking_description if not no_show else detail.seeking_description,
    'image_link': detail.Artist.image_link if not no_show else detail.image_link,
    'past_shows': past_shows,
    'upcoming_shows':upcoming_shows,
    'past_shows_count':len(past_shows),
    'upcoming_shows_count':len(upcoming_shows)
    }

  return render_template('pages/show_artist.html', artist=artist_info)

#edit artists

@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()  
  artist = Artist.query.get(artist_id)
  form.genres.data = artist.genres
    
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  form = ArtistForm(request.form)
  if form.validate():
    try:
      artist = Artist.query.get(artist_id)
      artist.name = form.name.data
      artist.city=form.city.data
      artist.state=form.state.data
      artist.phone=form.phone.data
      artist.genres=",".join(form.genres.data) 
      artist.facebook_link=form.facebook_link.data
      artist.image_link=form.image_link.data
      artist.seeking_venue=form.seeking_venue.data
      artist.seeking_description=form.seeking_description.data
      artist.website=form.website_link.data
      db.session.add(artist)
      db.session.commit()
      flash("Artist " + artist.name + " was successfully edited!")
    except:
      db.session.rollback()
      flash('Artist could not be edited successfully.')
    finally:
      db.session.close()
  else:
      flash('please submit valid form results')

  return redirect(url_for('show_artist', artist_id=artist_id))
 

#artist creation

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  form = ArtistForm(request.form)
  if form.validate():
    try:
      new_artist = Artist(
        name=form.name.data,
        city=form.city.data,
        state=form.state.data,
        phone=form.phone.data,
        genres=",".join(form.genres.data), 
        image_link=form.image_link.data,
        facebook_link=form.facebook_link.data,
        website=form.website_link.data,
        seeking_venue=form.seeking_venue.data,
        seeking_description=form.seeking_description.data,
      )
      db.session.add(new_artist)
      db.session.commit()
      flash("Artist " + request.form["name"] + " was successfully listed!")
    finally:
      db.session.close()
      return redirect(url_for('index'))
   
#show

@app.route('/shows')
def shows():
  data = []

  shows = Show.query.all()
  for show in shows:
    temp = {}
    temp["venue_id"] = show.venue.id
    temp["venue_name"] = show.venue.name
    temp["artist_id"] = show.artist.id
    temp["artist_name"] = show.artist.name
    temp["artist_image_link"] = show.artist.image_link
    temp["start_time"] = show.start_time.strftime("%m/%d/%Y, %H:%M:%S")
        
    data.append(temp)
    
  return render_template('pages/shows.html', shows=data)

#shows creation

@app.route('/shows/create')
def create_shows():
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  
  form = ShowForm(request.form)
  if form.validate():
    try:
      new_show = Show(
        artist_id=form.artist_id.data,
        venue_id=form.venue_id.data,
        start_time=form.start_time.data
      )
      db.session.add(new_show)
      db.session.commit()
      flash('Show was successfully listed!')
      
    except:
      flash('show could not be created successfully')
       
    finally:
      db.session.close()
      return render_template('pages/home.html')

  else:
    flash('please submit valid form results')
    return redirect(url_for('index'))

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

if __name__ == '__main__':
    app.run()

'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
