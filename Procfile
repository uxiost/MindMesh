release: cd frontend && npm install --prefix ./ && npm run build --prefix ./
web: cd backend && uvicorn mindmesh_app:app --host 0.0.0.0 --port ${PORT:-5000}