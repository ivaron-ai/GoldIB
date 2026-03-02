"""Infrastructure tests for Ralph.

These tests verify:
- Redis connection is reachable
- TimescaleDB connection is reachable  
- FastAPI endpoint /health returns 200
"""

import os
import pytest
import redis
import psycopg2
import httpx
from unittest.mock import patch


# Test configuration - uses environment variables or defaults to Docker Compose settings
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://ralph:ralph_secret@localhost:5432/ralph_db"
)
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")


class TestRedisConnection:
    """Tests for Redis connectivity."""

    def test_redis_connection_reachable(self):
        """Verify Redis connection is reachable."""
        try:
            client = redis.from_url(REDIS_URL, socket_timeout=5)
            response = client.ping()
            assert response is True, "Redis ping should return True"
        except redis.ConnectionError as e:
            pytest.skip(f"Redis not available: {e}")

    def test_redis_set_and_get(self):
        """Verify Redis can store and retrieve values."""
        try:
            client = redis.from_url(REDIS_URL, socket_timeout=5)
            client.ping()
            
            # Test set/get operations
            test_key = "ralph:test:key"
            test_value = "test_value_123"
            
            client.set(test_key, test_value)
            result = client.get(test_key)
            
            assert result.decode() == test_value
            
            # Cleanup
            client.delete(test_key)
        except redis.ConnectionError as e:
            pytest.skip(f"Redis not available: {e}")


class TestTimescaleDBConnection:
    """Tests for TimescaleDB (PostgreSQL) connectivity."""

    def _parse_database_url(self, url: str) -> dict:
        """Parse DATABASE_URL into connection parameters."""
        # Format: postgresql://user:password@host:port/dbname
        from urllib.parse import urlparse
        parsed = urlparse(url)
        return {
            "host": parsed.hostname or "localhost",
            "port": parsed.port or 5432,
            "user": parsed.username or "ralph",
            "password": parsed.password or "ralph_secret",
            "dbname": parsed.path.lstrip("/") or "ralph_db",
        }

    def test_timescaledb_connection_reachable(self):
        """Verify TimescaleDB connection is reachable."""
        try:
            params = self._parse_database_url(DATABASE_URL)
            conn = psycopg2.connect(**params, connect_timeout=5)
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            assert result[0] == 1, "Database should return 1"
            cursor.close()
            conn.close()
        except psycopg2.OperationalError as e:
            pytest.skip(f"TimescaleDB not available: {e}")

    def test_timescaledb_version(self):
        """Verify TimescaleDB version is accessible."""
        try:
            params = self._parse_database_url(DATABASE_URL)
            conn = psycopg2.connect(**params, connect_timeout=5)
            cursor = conn.cursor()
            cursor.execute("SELECT version()")
            result = cursor.fetchone()
            assert "PostgreSQL" in result[0], "Should be PostgreSQL"
            cursor.close()
            conn.close()
        except psycopg2.OperationalError as e:
            pytest.skip(f"TimescaleDB not available: {e}")


class TestFastAPIEndpoints:
    """Tests for FastAPI endpoints."""

    def test_health_endpoint_returns_200(self):
        """Verify /health endpoint returns 200."""
        try:
            with httpx.Client(timeout=5.0) as client:
                response = client.get(f"{API_BASE_URL}/health")
                assert response.status_code == 200, f"Expected 200, got {response.status_code}"
                
                data = response.json()
                assert data["status"] == "healthy"
                assert data["service"] == "ralph"
        except httpx.ConnectError as e:
            pytest.skip(f"API not available: {e}")

    def test_root_endpoint(self):
        """Verify root endpoint returns expected response."""
        try:
            with httpx.Client(timeout=5.0) as client:
                response = client.get(f"{API_BASE_URL}/")
                assert response.status_code == 200
                
                data = response.json()
                assert "message" in data
                assert "version" in data
        except httpx.ConnectError as e:
            pytest.skip(f"API not available: {e}")


class TestFastAPIApp:
    """Tests for FastAPI app using TestClient (no server required)."""

    def test_health_endpoint_unit(self):
        """Unit test for /health endpoint."""
        from fastapi.testclient import TestClient
        from src.api import app
        
        client = TestClient(app)
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "ralph"

    def test_root_endpoint_unit(self):
        """Unit test for root endpoint."""
        from fastapi.testclient import TestClient
        from src.api import app
        
        client = TestClient(app)
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Welcome to Ralph API"
        assert data["version"] == "0.1.0"
