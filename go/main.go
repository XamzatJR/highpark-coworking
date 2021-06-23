package main

import (
	"log"
	"net/http"
	"net/http/httputil"
	"net/url"
	"time"

	"github.com/gorilla/mux"
	"github.com/joho/godotenv"
)

var staticDir = "./static"
var htmlDir = staticDir + "/html/"
var origin, _ = url.Parse(Host())
var path = "/api/*catchall"
var reverseProxy = httputil.NewSingleHostReverseProxy(origin)

func init() {
	if err := godotenv.Load(); err != nil {
		log.Println("No .env file found")
	}
}

func main() {
	router := mux.NewRouter()
	router.NotFoundHandler = http.HandlerFunc(Custom404)
	reverseProxy.Director = Director

	router.PathPrefix("/static/").Handler(http.StripPrefix("/static/", http.FileServer(http.Dir(staticDir))))
	router.HandleFunc("/favicon.ico", FaviconHandler)
	router.HandleFunc("/", Index)
	router.HandleFunc("/profile", Profile)
	router.HandleFunc("/logout", Logout)
	router.HandleFunc("/{template}", DynamicTemplateHandler)
	router.PathPrefix("/api/").HandlerFunc(ApiReverseProxy)

	router.Use(RequestLoggerMiddleware(router))

	server := &http.Server{
		Handler:      router,
		Addr:         ":4000",
		WriteTimeout: 15 * time.Second,
		ReadTimeout:  15 * time.Second,
	}

	log.Fatal(server.ListenAndServe())
}
