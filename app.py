from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config.from_pyfile('config.cfg')
mysql = MySQL(app)
api = Api(app)

#class TopAmenities(Resource):

class TopAmenities(Resource):

    def get(self, user, limit):
        user_id = int(user)
        top = int(limit)

        cur = mysql.connection.cursor()
        cur.execute(f"""SELECT user_id, amenity_id, COUNT(amenity_id) AS amenity_count
                        FROM user_insights_system.selections 
                        WHERE user_id = {user_id} 
                        GROUP BY amenity_id 
                        ORDER BY amenity_count DESC
                        LIMIT {top}""")
        results = cur.fetchall()
        return jsonify(f'Below is the result generated for the top {top} amenities selected by user - {user_id}', results)

class TopHotels(Resource):
    
    def get(self, user, limit):
        user_id = int(user)
        top = int(limit)

        cur = mysql.connection.cursor()
        cur.execute(f"""SELECT user_id, hotel_id, COUNT(hotel_id) AS hotel_count
                        FROM user_insights_system.clicks 
                        WHERE user_id = {user_id}
                        GROUP BY hotel_id 
                        ORDER BY hotel_count DESC
                        LIMIT {top}""")
        results = cur.fetchall()
        return jsonify(f'Below is the result generated for the top {top} hotels selected by user - {user_id}', results)


api.add_resource(TopAmenities, '/amenities/<user>/<limit>')
api.add_resource(TopHotels, '/hotels/<user>/<limit>')

if __name__ == '__main__':
    app.run(debug=True)
