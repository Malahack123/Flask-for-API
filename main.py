from flask import Flask, session
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask('app')
api = Api(app)
app.config['SECRET_KEY'] = 'kali-malahack@123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite3.db'
app.config['SQLALCHEMY_MODIFICATIONS_TRACKS'] = False
db = SQLAlchemy(app)


class VideoModel(db.Model):
  _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(100), nullable=False)
  views = db.Column(db.Integer, nullable=False)
  likes = db.Column(db.Integer, nullable=False)

  def __repr__(self):
    return f"Video(name={self.name}, views={self.views}, likes={self.likes})"


video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name",
                            type=str,
                            help="Name of the video",
                            required=True)
video_put_args.add_argument("likes",
                            type=int,
                            help="Number of likes",
                            required=True)
video_put_args.add_argument("views",
                            type=int,
                            help="Number of views",
                            required=True)
video_update_args= reqparse.ReqParser()
video_update_args.add_argument(name",
                            type=str,
                            help="Name of the video",
                            required=True")   
video_update_args.add_argument("likes",
                            type=int,
                            help="Number of likes",
                            required=True)
video_update_args.add_argument("views",
                            type=int,
                            help="Number of views",
                            required=True)


videos = {}


def abort_if_video_doesnt_exist(video_id):
  if video_id not in videos:
    abort(404, message="Video doesnt exist")


def abort_if_video_exists(video_id):
  if video_id in videos:
    abort(409, message="Video already exists")


result = None
resource_fields = {
  'id': fields.Integer,
  'name': fields.String,
  'likes': fields.Integer,
  'views': fields.Integer
}


class Video(Resource):

  @marshal_with(resource_fields)
  def get(self, video_id):
    result = VideoModel.query.filter_by(id=video_id).first()
    if not result:
      abort(404, "NOT FOUND")
    return result

  @marshal_with(resource_fields)
  def put(self, video_id):
    abort_if_video_exists(video_id)
    args = video_put_args.parse_args()
    video = VideoModel(id=video_id,
                       name=args['name'],
                       views=args['views'],
                       likes=args['likes'])
    db.session.add(video)
    db.session.commit()
    return videos[video_id], 201
  def patch(self) :
    args = video_update_args.parse_args()
    result = VideoModel.query.filter_by(id=video_id).first()
    if not result:
      abort(404, "NOT FOUND")
    if args["name"]:
      result.name = args["name"]
    if args["likes"] :
      result.likes = args["likes"]
    if args["views"] :
      result.views = args["views"]
    db.session.commit()
    return result
  def delete(self, video_id):
    abort_if_video_exists(video_id)
    del videos[video_id]
    return '', 204

api.add_resource(Video, "/video/<int:video_id>")

app.run(host='0.0.0.0', port=8080, debug=True)
