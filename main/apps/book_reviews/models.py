# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re, md5, os, binascii

class UserManager(models.Manager):
	def length_within_range(self, val, min, max):
		return len(val) >= min and len(val) <= max

	def valid_email_address(self, email_address):
		email_validator = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

		return re.match(email_validator, email_address)

	def register(self, POST):
		response = {
			"response_type": "registration",
			"success": True,
			"errors": [],
			"user_id": None,
			"user_name": None
		}

		# Ensure complete form submission

		if (not "first_name" in POST
		or not "last_name" in POST
		or not "email_address" in POST
		or not "password" in POST
		or not "confirm_password" in POST):
			response["success"] = False
			response["errors"] += ["Incomplete form submission."]

			return response

		# Strip whitespace and set email to lowercase
		# (new variables because QueryDict is immutable)

		first_name = POST["first_name"].rstrip()
		last_name = POST["last_name"].rstrip()
		email_address = POST["email_address"].rstrip().lower()

		# Validate name

		if not self.length_within_range(first_name, 2, 75):
			response["success"] = False
			response["errors"] += ["First name must be within 2-75 characters."]

		if not self.length_within_range(last_name, 2, 75):
			response["success"] = False
			response["errors"] += ["Last name must be within 2-75 characters."]

		# Validate email address

		if not self.length_within_range(email_address, 0, 255):
			response["success"] = False
			response["errors"] += ["Email address must be 255 or fewer characters."]

		if not self.valid_email_address(email_address):
			response["success"] = False
			response["errors"] += ["Email address must be valid."]

		if self.filter(email_address=email_address).exists():
			response["success"] = False
			response["errors"] += ["The specified email address is already in use."]

		# Validate password

		if not self.length_within_range(POST["password"], 8, 255):
			response["success"] = False
			response["errors"] += ["Password must be within 8-255 characters."]

		if not POST["password"] == POST["confirm_password"]:
			response["success"] = False
			response["errors"] += ["Passwords must match."]

		# Create User

		if response["success"]:
			password_salt = binascii.b2a_hex(os.urandom(15))
			password_hash = md5.new(POST["password"] + password_salt).hexdigest()

			user = User.objects.create(
				first_name = first_name,
				last_name = last_name,
				email_address = email_address,
				password_hash = password_hash,
				password_salt = password_salt
			)

			response["user_id"] = user.id
			response["user_name"] = user.first_name


		return response

	def login(self, POST):
		response = {
			"response_type": "login",
			"success": True,
			"errors": [],
			"user_id": None,
			"user_name": None
		}

		if (not "email_address" in POST
		or not "password" in POST):
			response["success"] = False
			response["errors"] += ["Incomplete form submission."]

			return response

		email_address = POST["email_address"].rstrip().lower()
		user = User.objects.filter(email_address=email_address).first()

		if not user:
			response["success"] = False
			response["errors"] += ["There is no account with the specified email address."]

			return response

		password_hash = md5.new(POST["password"] + user.password_salt).hexdigest()

		if not password_hash == user.password_hash:
			response["success"] = False
			response["errors"] += ["Incorrect password."]

		response["user_id"] = user.id
		response["user_name"] = user.first_name

		return response

class User(models.Model):
	first_name = models.CharField(max_length=75)
	last_name = models.CharField(max_length=75)
	email_address = models.CharField(max_length=255)
	password_hash = models.CharField(max_length=32)
	password_salt = models.CharField(max_length=32)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = UserManager()

class BookManager(models.Manager):
	def length_within_range(self, val, min, max):
		return len(val) >= min and len(val) <= max

	def addReview(self, POST, poster_id):
		response = {
			"response_type": "review-submission",
			"success": True,
			"errors": [],
			"book": None,
			"review": None
		}

		# Ensure complete form submission

		if (not "title" in POST
		or not "author" in POST
		or not "rating" in POST
		or not "review" in POST):
			response["success"] = False
			response["errors"] += ["Incomplete form submission."]

			return response

		title = POST["title"].rstrip().upper()
		author = POST["author"].rstrip().upper()
		rating = int(POST["rating"])
		review_text = POST["review"].rstrip()

		# Validate

		if not self.length_within_range(title, 2, 255):
			response["success"] = False
			response["errors"] += ["Title must be within 2-255 characters."]

		if not self.length_within_range(author, 2, 255):
			response["success"] = False
			response["errors"] += ["Author must be within 2-255 characters."]

		if not self.length_within_range(review_text, 2, 255):
			response["success"] = False
			response["errors"] += ["Review must be within 2-255 characters."]

		# Create the review (and book if not found)

		book = Book.objects.filter(title=title, author=author).first()

		if not book:
			book = Book.objects.create(title=title, author=author)

		poster = User.objects.filter(id=poster_id).first()

		if not poster:
			response["success"] = False
			response["errors"] = ["HACKER BAD >:("]

		if response["success"]:
			response["book"] = book
			response["review"] = book.reviews.create(rating=rating, review_text=review_text, poster=poster)

		return response


class Book(models.Model):
	title = models.CharField(max_length=255)
	author = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = BookManager()

class Review(models.Model):
	rating = models.IntegerField()
	review_text = models.CharField(max_length=255)
	book = models.ForeignKey(Book, related_name="reviews")
	poster = models.ForeignKey(User, related_name="reviews")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)