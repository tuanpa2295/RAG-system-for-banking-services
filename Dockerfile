# Use the official PostgreSQL image as base
FROM postgres:15

# Set environment variables for Postgres
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres
ENV POSTGRES_DB=banking_rag

# Expose PostgreSQL port
EXPOSE 5432
