package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"net/http"

	"github.com/gorilla/mux"
)

func faviconHandler(w http.ResponseWriter, r *http.Request) {
	http.ServeFile(w, r, staticDir+"/favicon.ico")
}

func index(w http.ResponseWriter, r *http.Request) {
	html, err := ioutil.ReadFile(htmlDir + "index.html")
	if err != nil {
		log.Println(err)
	}
	fmt.Fprint(w, string(html))
}

func dynamicTemplateHandler(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	html, err := ioutil.ReadFile(htmlDir + vars["template"] + ".html")
	if err != nil {
		log.Println(err)
		custom404(w, r)
	}
	fmt.Fprint(w, string(html))
}

func logout(w http.ResponseWriter, r *http.Request) {
	c := http.Cookie{
		Name:   "Authorization",
		MaxAge: -1}
	http.SetCookie(w, &c)
	http.Redirect(w, r, "/", http.StatusSeeOther)
}

func apiReverseProxy(w http.ResponseWriter, r *http.Request) {
	cookie, err := r.Cookie("Authorization")
	if err != nil {
		reverseProxy.ServeHTTP(w, r)
		return
	}
	r.Header.Add(cookie.Name, cookie.Value)
	reverseProxy.ServeHTTP(w, r)
}

func custom404(w http.ResponseWriter, req *http.Request) {
	html, err := ioutil.ReadFile(htmlDir + "404.html")
	if err != nil {
		log.Println(err)
	}
	fmt.Fprint(w, string(html))
}
