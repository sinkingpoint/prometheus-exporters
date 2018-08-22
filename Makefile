image:
	docker build -t sinkingpoint/utilities_exporter:master .

push: image
	docker push sinkingpoint/utilities_exporter:master
