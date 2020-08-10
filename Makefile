#~/P/W/aio ❯❯❯ twine upload dist/*                                                                                                                                                                                                                                                                                           ⏎
#~/P/W/aio ❯❯❯ python3 setup.py sdist bdist_wheel                                                                                                                                                                                                                                                                            ⏎
#~/P/W/aio ❯❯❯ rm -rf aio-geojson-query.egg-info build dist

all: aio-geojson-query.egg-info

aio-geojson-query.egg-info:
	python3 setup.py sdist bdist_wheel

clean:
	rm -rf aio-geojson-query.egg-info build dist

push:
	twine upload dist/*
