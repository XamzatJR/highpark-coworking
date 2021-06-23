package main

import (
	"log"
	"net/http"
	"os"
	"strings"

	"github.com/gbrlsnchs/jwt/v3"
	"github.com/gorilla/mux"
)

var hs = jwt.NewHS256([]byte(SecretKey()))

type CustomPayload struct {
	jwt.Payload
	Email string `json:"email"`
}

func RequestLoggerMiddleware(r *mux.Router) mux.MiddlewareFunc {
	return func(next http.Handler) http.Handler {
		return http.HandlerFunc(func(w http.ResponseWriter, req *http.Request) {
			defer func() {
				log.Printf(
					"[%s] %s %s %s",
					req.Method,
					req.Host,
					req.URL.Path,
					req.URL.RawQuery,
				)
			}()

			next.ServeHTTP(w, req)
		})
	}
}

func CheckJwt(w http.ResponseWriter, r *http.Request) {
	var pl CustomPayload
	c, err := r.Cookie("Authorization")
	if err != nil {
		http.Redirect(w, r, "/login", http.StatusSeeOther)
	}
	token := []byte(c.Value[7:])
	hd, err := jwt.Verify(token, hs, &pl)
	if err != nil {
		http.Redirect(w, r, "/login", http.StatusSeeOther)
	}
	log.Println(hd)
}

func Director(r *http.Request) {
	r.Header.Add("X-Forwarded-Host", r.Host)
	r.Header.Add("X-Origin-Host", origin.Host)
	r.URL.Scheme = origin.Scheme
	r.URL.Host = origin.Host

	wildcardIndex := strings.IndexAny(path, "*")
	proxyPath := SingleJoiningSlash(origin.Path, r.URL.Path[wildcardIndex:])
	if strings.HasSuffix(proxyPath, "/") && len(proxyPath) > 1 {
		proxyPath = proxyPath[:len(proxyPath)-1]
	}
	r.URL.Path = proxyPath
}

func Host() string {
	val, ok := os.LookupEnv("api_host")
	if !ok {
		return "http://127.0.0.1:8000/"
	}
	return val
}

func SecretKey() string {
	val, ok := os.LookupEnv("secret_key")
	if !ok {
		log.Fatalln("Error: variable secret key not in .env")
	}
	return val
}

func SingleJoiningSlash(a, b string) string {
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
