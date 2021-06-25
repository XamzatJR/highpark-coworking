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

var staticDir string
var htmlDir string
var origin *url.URL
var path string
var reverseProxy *httputil.ReverseProxy

func init() {
	if err := godotenv.Load(); err != nil {
		log.Fatalln("No .env file found")
	}
	staticDir = "./static"
	htmlDir = staticDir + "/html/"
	origin, _ = url.Parse(Host())
	path = "/api/*catchall"
	reverseProxy = httputil.NewSingleHostReverseProxy(origin)
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

	err := server.ListenAndServe()
	if err != nil {
		log.Fatal(err)
	}
}
