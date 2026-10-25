.PHONY: all test test-verbose install install-user uninstall clean build-rpm demo

all: test

test:
	@bash scripts/run-tests.sh

test-verbose:
	@python3 -m unittest discover -s tests -v

install-user:
	@bash desktop-installer/install.sh --user

install:
	@bash desktop-installer/install.sh --system

uninstall:
	@bash desktop-installer/uninstall.sh

demo:
	@bash scripts/launch-demo.sh

build-rpm:
	@bash desktop-packaging/build-rpm.sh

clean:
	@rm -rf build/ dist/ __pycache__ */__pycache__ */*/__pycache__
