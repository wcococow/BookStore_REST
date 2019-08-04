from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

#Init app
app = Flask(__name__);
basedir = os.path.abspath(os.path.dirname(__file__))
#setup database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SALALCHEMY_TRACK_MODIFICATIONS'] = False
#Init db
db = SQLAlchemy(app)
#Init ma
ma = Marshmallow(app)

subs = db.Table('subs',
				db.Column('author_id',db.Integer,db.ForeignKey('author.author_id')),
				db.Column('publication_id',db.Integer,db.ForeignKey('publication.publication_id'))
)
				
#Author class/model
class Author(db.Model):
	__tablename__ = 'author'
	author_id = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String(20))
	email = db.Column(db.String(30),unique=True)
	publication = db.relationship('Publication',secondary=subs,backref=db.backref('authors',lazy='dynamic'))
	def __init__(self,name,email):
		self.name = name
		self.email = email

#Author Schema
class AuthorSchema(ma.Schema):
	class Meta:
		fields = ('author_id','name','email');
#Init Author schema
author_schema = AuthorSchema(strict=True)
authors_schema = AuthorSchema(many=True,strict=True)
	
#Publication class/model
class Publication(db.Model):
	__tablename__ = 'publication'
	publication_id = db.Column(db.Integer,primary_key=True)
	catagory = db.Column(db.String(10))
	title = db.Column(db.String(30))
	year = db.Column(db.Integer)
	type = db.Column(db.String(20))
	hero = db.Column(db.String(20))
	genre = db.Column(db.String(10))
	
	def __init__(self,catagory,title,year,type,hero,genre):
		self.catagory = catagory
		self.title = title
		self.year = year
		self.type = type
		self.hero = hero
		self.genre = genre
		
#Publication Schema
class PublicationSchema(ma.Schema):
	class Meta:
		fields = ('publication_id','catagory','title','year','type','hero','genre');
#Init Publication schema
publication_schema = PublicationSchema(strict=True)
publications_schema = PublicationSchema(many=True,strict=True)
	

#create a author
@app.route('/author',methods=['POST'])
def add_author():
	name = request.json['name']
	email = request.json['email']
	
	new_author = Author(name,email)
	db.session.add(new_author)
	db.session.commit()
	
	return author_schema.jsonify(new_author)
	
#get all authors
@app.route('/author',methods=['GET'])
def get_authors():
	all_authors = Author.query.all()
	result = authors_schema.dump(all_authors)
	return jsonify(result.data)
	
#get single author
@app.route('/author/<id>',methods=['GET'])
def get_author(id):
	author = Author.query.get(id)
	return author_schema.jsonify(author)

#update author
@app.route('/author/<id>',methods=['PUT'])
def update_author(id):
	author = Author.query.get(id)
	
	name = request.json['name']
	email = request.json['email']
	
	author.name = name
	author.email = email
	
	db.session.commit()
	
	return author_schema.jsonify(author)

#delete author
@app.route('/author/<id>',methods=['DELETE'])
def delete_author(id):
	author = Author.query.get(id)
	db.session.delete(author)
	db.session.commit()
	return author_schema.jsonify(author)	

#create a publication
@app.route('/publication',methods=['POST'])
def add_publication():
	catagory = request.json['catagory']
	title = request.json['title']
	year = request.json['year']
	type = request.json['type']
	hero = request.json['hero']
	genre = request.json['genre']
	
	new_publication = Publication(catagory,title,year,type,hero,genre)
	db.session.add(new_publication)
	db.session.commit()
	
	return publication_schema.jsonify(new_publication)
	
#get all publications
@app.route('/publication',methods=['GET'])
def get_publications():
	all_publications = Publication.query.all()
	result = publications_schema.dump(all_publications)
	return jsonify(result.data)

#get single publication
@app.route('/publication/<id>',methods=['GET'])
def get_publication(id):
	publication = Publication.query.get(id)
	return publication_schema.jsonify(publication)

#update publication
@app.route('/publication/<id>',methods=['PUT'])
def update_publication(id):
	publication = Publication.query.get(id)
	
	catagory = request.json['catagory']
	title = request.json['title']
	year = request.json['year']
	type = request.json['type']
	hero = request.json['hero']
	genre = request.json['genre']
	
	publication.catagory = catagory
	publication.title = title
	publication.year = year
	publication.type = type
	publication.hero = hero
	publication.genre = genre
	
	db.session.commit()
	
	return publication_schema.jsonify(publication)

#delete publication
@app.route('/publication/<id>',methods=['DELETE'])
def delete_publication(id):
	publication = Publication.query.get(id)
	db.session.delete(publication)
	db.session.commit()
	return publication_schema.jsonify(publication)		
#Run server
if  __name__ == '__main__':
	app.run(debug=True)