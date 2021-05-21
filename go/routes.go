package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
)

func index(w http.ResponseWriter, r *http.Request) {
	html, err := ioutil.ReadFile(htmlDir + "index.html")
	if err != nil {
		log.Fatalln(err)
	}
	fmt.Fprint(w, string(html))
}

func login(w http.ResponseWriter, r *http.Request) {
	html, err := ioutil.ReadFile(htmlDir + "login.html")
	if err != nil {
		log.Fatalln(err)
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
