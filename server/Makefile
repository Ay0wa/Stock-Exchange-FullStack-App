.PHONY: test coverage open-coverage clean

test:
	pytest --cov=. --cov-report=html

open-coverage:
	@if [ -f htmlcov/index.html ]; then \
		if [ -n "$$WSL_DISTRO_NAME" ]; then \
			explorer.exe $$(wslpath -w htmlcov/index.html); \
		elif [ "$$(uname)" = "Darwin" ]; then \
			open htmlcov/index.html; \
		elif [ "$$(uname)" = "Linux" ]; then \
			xdg-open htmlcov/index.html || sensible-browser htmlcov/index.html; \
		fi \
	else \
		echo "Сначала запустите make test для генерации отчета"; \
	fi

coverage: test open-coverage

clean:
	rm -rf htmlcov
	rm -f .coverage