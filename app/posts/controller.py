from flask import jsonify, request
from app import db
from posts.models import Messages
from geoalchemy2.elements import WKTElement
from geoalchemy2.functions import ST_DWithin
import math
from app import app

@app.route('/post_message',methods=['POST'])
def postmessage():
    data = request.get_json()
    message = data['message']
    lat = data['lat']
    lon = data['long']
    point = WKTElement(f'POINT({lon} {lat})', srid=4326)
    user=Messages(message=message,location=point)
    db.session.add(user)
    db.session.commit()
    return "successfully posted"


@app.route('/nearbypost/', methods=['GET'])
def getnearbypost():
    args=request.args
    lat=0
    lon=0
    for key,value in args.items():
        if key == 'lat':
            lat=value
        else:
            lon=value
    # Convert lat and lon to a point
    point = WKTElement(f'POINT({lon} {lat})', srid=4326)

    # Define the search radius in meters
    radius = 5000

    page = request.args.get('page', default=1, type=int)

    # Calculate the offset based on the current page number and the number of posts per page
    per_page = 10
    offset = (page - 1) * per_page

    # Query the database for posts within the search radius, limit the results to 10 per page
    posts = Messages.query.filter(ST_DWithin(Messages.location, point, radius)).offset(offset).limit(per_page).all()
    print(posts)
    # Get the total number of posts within the search radius
    total_posts = Messages.query.filter(ST_DWithin(Messages.location, point, radius)).count()

    # Calculate the total number of pages
    total_pages = int(math.ceil(total_posts / per_page))

    # Serialize the posts to JSON and return the response
    return jsonify({
        'posts': [post.to_dict() for post in posts],
        'current_page': page,
        'total_pages': total_pages,
        'total_posts': total_posts
    })

