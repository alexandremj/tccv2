install_deps:
	uv pip install -r pyproject.toml
run_server:
	uv run fastapi dev
setup:
	./scripts/setup.sh
deploy_contracts:
	python3 ./scripts/deploy.py
refresh_token:
	export TOKEN=$(http --form POST :8000/token username="test@user.com" password="test_password" | jq -r '.access_token')
