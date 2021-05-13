package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
)

var static = "./static/html/"

func index(w http.ResponseWriter, r *http.Request) {
	html, err := ioutil.ReadFile(static + "index.html")
	if err != nil {
		log.Fatalln(err)
	}
	fmt.Fprint(w, string(html))
}

func main() {
	mux := http.NewServeMux()
	fileserver := http.FileServer(http.Dir("./static"))

	mux.Handle("/static/", http.StripPrefix("/static", fileserver))

	mux.HandleFunc("/", index)
	http.ListenAndServe(":4000", mux)
}
