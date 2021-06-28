package main

import (
	"encoding/json"
	"log"
	"net/http"
	"os"
	"strings"

	"github.com/gorilla/mux"
)

type TokenVerify struct {
	Valid bool `json:"valid"`
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

func IsAuthenticated(r *http.Request) bool {
	c, err := r.Cookie("access_token_cookie")
	if err != nil {
		return false
	}
	cookie := &http.Cookie{
		Name:   c.Name,
		Value:  c.Value,
		MaxAge: 300,
	}
	req, err := http.NewRequest("POST", Host()+"/auth/verify", nil)
	req.Header.Add("X-Sender", "golangserver")
	if err != nil {
		log.Fatalln(err)
	}
	req.AddCookie(cookie)
	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		log.Fatalln(err)
	}
	var result TokenVerify

	json.NewDecoder(resp.Body).Decode(&result)
	return result.Valid
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
		return "http://127.0.0.1:8000"
	}
	return val
}

func SecretKey() []byte {
	val, ok := os.LookupEnv("authjwt_secret_key")
	if !ok {
		log.Fatalln("Error: variable authjwt_secret_key not in .env")
	}
	return []byte(val)
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
