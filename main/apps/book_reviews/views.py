# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from .models import User, Book, Review

def index(request):
	if "user_id" in request.session:
		return redirect("/reviews")

	return render(request, "index.html")

def register(request):
	if request.method == "POST":
		response = User.objects.register(request.POST)

		if not response["success"]:
			return render(request, "index.html", response)

		request.session["user_id"] = response["user_id"]
		request.session["user_name"] = response["user_name"]

	return redirect("/reviews")

def login(request):
	if request.method == "POST":
		response = User.objects.login(request.POST)

		if not response["success"]:
			return render(request, "index.html", response)

		request.session["user_id"] = response["user_id"]
		request.session["user_name"] = response["user_name"]

	return redirect("/reviews")

def logout(request):
	request.session.flush()

	return redirect("/")

def new_review(request):
	if "user_id" in request.session:
		return render(request, "new.html", { "user_name": request.session["user_name"] })

	if not response["success"]:
		response["user_name"] = request.session["user_name"]
		return render(request, "new.html", response)

	return redirect("/")

def new_review_submit(request):
	if "user_id" in request.session:
		if request.method == "POST":
			response = Book.objects.addReview(request.POST, request.session["user_id"])

		if not response["success"]:
			response["user_name"] = request.session["user_name"]
			return render(request, "new.html", response)

		return redirect("/reviews")

	return redirect("/")

def reviews(request):
	context = { # check out that extended slice operation
		"recent": Review.objects.all()[::-1][:3],
		"all_books": Book.objects.all()[::-1],
		"user_name": request.session["user_name"]
	}

	return render(request, "reviews.html", context)

def reviews_for_book(request, book_id):
	book = Book.objects.filter(id=book_id).first()

	if book:
		context = {
			"book": book,
			"all_reviews": Review.objects.filter(book=book),
			"user_name": request.session["user_name"]
		}

		return render(request, "book.html", context)
	
	return redirect("/")