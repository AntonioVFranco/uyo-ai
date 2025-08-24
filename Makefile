
    .PHONY: fmt lint test ci run-api run-ui

    VENV?=.venv

    fmt:
	black .
	ruff check --fix .

    lint:
	ruff check .
	black --check .

    test:
	pytest -q

    ci: lint test

    run-api:
	uvicorn apps.uyo_ai_api.app:app --reload

    run-ui:
	streamlit run apps/uyo_ai_ui/app.py
