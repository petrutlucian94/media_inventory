#!/bin/bash

# curl 127.0.0.1:5000/movies -X POST -d @test_movie --header "Content-Type:application/xml"
curl 127.0.0.1:5000/movies/1cb47ab2-4ad2-490f-af77-da2b23dbaf42 --header "Content-Type:application/xml"
