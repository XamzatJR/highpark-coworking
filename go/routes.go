package main

import (
	"log"
	"net/http"
	"path/filepath"
	"text/template"

	"github.com/gorilla/mux"
)

type RequestData struct {
	Authenticated bool
}

func FaviconHandler(w http.ResponseWriter, r *http.Request) {
	path := filepath.Join(staticDir, "favicon.ico")
	http.ServeFile(w, r, path)
}

func Index(w http.ResponseWriter, r *http.Request) {
	path := filepath.Join(htmlDir, "index.html")
	tmpl, _ := template.ParseFiles(path)

	data := RequestData{IsAuthenticated(r)}
	err := tmpl.Execute(w, data)
	if err != nil {
		log.Panic(err.Error())
	}
}

func Profile(w http.ResponseWriter, r *http.Request) {
	result := IsAuthenticated(r)
	if !result {
		http.Redirect(w, r, "/login", http.StatusSeeOther)
		return
	}
	path := filepath.Join(htmlDir, "profile.html")
	tmpl, _ := template.ParseFiles(path)

	data := RequestData{IsAuthenticated(r)}
	err := tmpl.Execute(w, data)
	if err != nil {
		log.Println(err.Error())
		NotFoundHandler(w, r)
	}
}

func DynamicTemplateHandler(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	if (vars["template"] == "login" || vars["template"] == "register") && IsAuthenticated(r) {
		http.Redirect(w, r, "/profile", http.StatusSeeOther)
		return
	}
	path := filepath.Join(htmlDir, vars["template"]+".html")
	tmpl, err := template.ParseFiles(path)
	if err != nil {
		log.Println(err.Error())
		NotFoundHandler(w, r)
	}

	data := RequestData{IsAuthenticated(r)}
	tmpl.Execute(w, data)
}

func Logout(w http.ResponseWriter, r *http.Request) {
	c := http.Cookie{
		Name:   "access_token_cookie",
		MaxAge: -1}
	http.SetCookie(w, &c)
	http.Redirect(w, r, "/", http.StatusSeeOther)
}

func ApiReverseProxy(w http.ResponseWriter, r *http.Request) {
	reverseProxy.ServeHTTP(w, r)
}

func NotFoundHandler(w http.ResponseWriter, r *http.Request) {
	path := filepath.Join(htmlDir, "404.html")
	tmpl, _ := template.ParseFiles(path)
	_ = tmpl.Execute(w, nil)
}
