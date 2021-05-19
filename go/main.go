package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"net/http/httputil"
	"net/url"
	"os"
	"strings"
	"time"

	"github.com/gorilla/mux"
	"github.com/joho/godotenv"
)

var staticDir = "./static"
var htmlDir = staticDir + "/html/"

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

func singleJoiningSlash(a, b string) string {
	aslash := strings.HasSuffix(a, "/")
	bslash := strings.HasPrefix(b, "/")
	switch {
	case aslash && bslash:
		return a + b[1:]
	case !aslash && !bslash:
		return a + "/" + b
	}
	return a + b
}

func init() {
	if err := godotenv.Load(); err != nil {
		log.Println("No .env file found")
	}
}

func main() {
	router := mux.NewRouter()

	host := func() string {
		val, ok := os.LookupEnv("api_host")
		if !ok {
			return "http://127.0.0.1:8000/"
		}
		return val
	}

	origin, _ := url.Parse(host())

	path := "/api/*catchall"

	reverseProxy := httputil.NewSingleHostReverseProxy(origin)
	reverseProxy.Director = func(r *http.Request) {
		r.Header.Add("X-Forwarded-Host", r.Host)
		r.Header.Add("X-Origin-Host", origin.Host)
		r.URL.Scheme = origin.Scheme
		r.URL.Host = origin.Host

		wildcardIndex := strings.IndexAny(path, "*")
		proxyPath := singleJoiningSlash(origin.Path, r.URL.Path[wildcardIndex:])
		if strings.HasSuffix(proxyPath, "/") && len(proxyPath) > 1 {
			proxyPath = proxyPath[:len(proxyPath)-1]
		}
		r.URL.Path = proxyPath
	}

	router.PathPrefix("/static/").Handler(http.StripPrefix("/static/", http.FileServer(http.Dir(staticDir))))
	router.HandleFunc("/", index)
	router.HandleFunc("/login", login)
	router.HandleFunc("/logout", func(w http.ResponseWriter, r *http.Request) {
		c := http.Cookie{
			Name:   "Authorization",
			MaxAge: -1}
		http.SetCookie(w, &c)
		http.Redirect(w, r, "/", http.StatusSeeOther)
	})
	router.PathPrefix("/api/").HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		cookie, err := r.Cookie("Authorization")
		if err != nil {
			reverseProxy.ServeHTTP(w, r)
			return
		}
		r.Header.Add(cookie.Name, cookie.Value)
		reverseProxy.ServeHTTP(w, r)
	})

	server := &http.Server{
		Handler:      router,
		Addr:         ":4000",
		WriteTimeout: 15 * time.Second,
		ReadTimeout:  15 * time.Second,
	}

	log.Fatal(server.ListenAndServe())
}
