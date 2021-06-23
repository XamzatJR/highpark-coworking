package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"net/http"

	"github.com/gorilla/mux"
)

func FaviconHandler(w http.ResponseWriter, r *http.Request) {
	http.ServeFile(w, r, staticDir+"/favicon.ico")
}

func Index(w http.ResponseWriter, r *http.Request) {
	CheckJwt(w, r)
	html, err := ioutil.ReadFile(htmlDir + "index.html")
	if err != nil {
		log.Println(err)
	}
	fmt.Fprint(w, string(html))
}

func Profile(w http.ResponseWriter, r *http.Request) {
	html, err := ioutil.ReadFile(htmlDir + "profile.html")
	if err != nil {
		log.Println(err)
	}
	fmt.Fprint(w, string(html))
}

func DynamicTemplateHandler(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	html, err := ioutil.ReadFile(htmlDir + vars["template"] + ".html")
	if err != nil {
		log.Println(err)
		Custom404(w, r)
	}
	fmt.Fprint(w, string(html))
}

func Logout(w http.ResponseWriter, r *http.Request) {
	c := http.Cookie{
		Name:   "Authorization",
		MaxAge: -1}
	http.SetCookie(w, &c)
	http.Redirect(w, r, "/", http.StatusSeeOther)
}

func ApiReverseProxy(w http.ResponseWriter, r *http.Request) {
	cookie, err := r.Cookie("Authorization")
	if err != nil {
		reverseProxy.ServeHTTP(w, r)
		return
	}
	r.Header.Add(cookie.Name, cookie.Value)
	reverseProxy.ServeHTTP(w, r)
}

func Custom404(w http.ResponseWriter, req *http.Request) {
	html, err := ioutil.ReadFile(htmlDir + "404.html")
	if err != nil {
		log.Println(err)
	}
	fmt.Fprint(w, string(html))
}
